module.exports = function (eleventyConfig) {
  // Static assets -> output root
  eleventyConfig.addPassthroughCopy({ "static/admin": "admin" });
  eleventyConfig.addPassthroughCopy({ "static/css": "css" });
  // Decap uploads land in src/img, served at /img
  eleventyConfig.addPassthroughCopy({ "src/img": "img" });

  const isoDate = (v) => {
    if (!v) return "";
    if (v instanceof Date) return v.toISOString().slice(0, 10);
    const s = String(v).trim();
    const m = s.match(/^(\d{4})-(\d{2})-(\d{2})/);
    return m ? `${m[1]}-${m[2]}-${m[3]}` : s;
  };
  const todayStr = () => new Date().toISOString().slice(0, 10);

  eleventyConfig.addFilter("isoDate", isoDate);
  eleventyConfig.addFilter("year", (v) => isoDate(v).slice(0, 4));
  eleventyConfig.addFilter("readableDate", (v) => {
    const iso = isoDate(v);
    const m = iso.match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (!m) return iso;
    const d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
    return d.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric",
      timeZone: "UTC",
    });
  });
  eleventyConfig.addFilter("byArtist", (events, name) =>
    (events || []).filter((e) => (e.data.artist || "") === name)
  );

  // Drafts: excluded from listings and not written as pages.
  // publish_at: event stays hidden until that moment (Toronto wall time if
  // no offset given); unparseable embargo values stay hidden (fail closed).
  const nthSundayUTC = (y, m, n) => {
    const first = 1 + ((7 - new Date(Date.UTC(y, m, 1)).getUTCDay()) % 7);
    return new Date(Date.UTC(y, m, first + 7 * (n - 1)));
  };
  const torontoOffsetMinutes = (d) => {
    const y = d.getUTCFullYear();
    const start = nthSundayUTC(y, 2, 2); start.setUTCHours(7); // 2nd Sun Mar, 2am local
    const end = nthSundayUTC(y, 10, 1); end.setUTCHours(6);   // 1st Sun Nov, 2am local
    return d >= start && d < end ? -240 : -300;
  };
  const publishTime = (v) => {
    if (!v) return null;
    if (v instanceof Date) return isNaN(v) ? null : v;
    const s = String(v).trim();
    if (/[zZ]|[+-]\d{2}:?\d{2}$/.test(s)) {
      const t = new Date(s);
      return isNaN(t) ? null : t;
    }
    const m = s.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2}))?/);
    if (!m) return null;
    const d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3], +m[4], +m[5], +(m[6] || 0)));
    return new Date(d.getTime() - torontoOffsetMinutes(d) * 60000);
  };
  const isLive = (e) => {
    if (e.data.draft) return false;
    if (!e.data.publish_at) return true;
    const t = publishTime(e.data.publish_at);
    return !!t && t <= new Date();
  };
  const notDraft = (items) => (items || []).filter(isLive);
  eleventyConfig.addGlobalData("eleventyComputed", {
    permalink: (data) => (data.draft ? false : data.permalink),
  });

  const byDateDesc = (a, b) => (isoDate(a.data.date) < isoDate(b.data.date) ? 1 : -1);

  eleventyConfig.addCollection("allEvents", (c) =>
    notDraft(c.getFilteredByGlob("src/events/*.md")).sort(byDateDesc)
  );
  eleventyConfig.addCollection("upcomingEvents", (c) => {
    const t = todayStr();
    return notDraft(c.getFilteredByGlob("src/events/*.md"))
      .filter((e) => isoDate(e.data.date) >= t)
      .sort(byDateDesc);
  });
  eleventyConfig.addCollection("pastEvents", (c) => {
    const t = todayStr();
    return notDraft(c.getFilteredByGlob("src/events/*.md"))
      .filter((e) => isoDate(e.data.date) < t)
      .sort(byDateDesc);
  });
  eleventyConfig.addCollection("artistsList", (c) =>
    notDraft(c.getFilteredByGlob("src/artists/*.md")).sort((a, b) =>
      (a.data.name || "").localeCompare(b.data.name || "")
    )
  );

  return {
    dir: { input: "src", output: "_site", includes: "_includes" },
  };
};
