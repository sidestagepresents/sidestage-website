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

  const byDateDesc = (a, b) => (isoDate(a.data.date) < isoDate(b.data.date) ? 1 : -1);

  eleventyConfig.addCollection("allEvents", (c) =>
    c.getFilteredByGlob("src/events/*.md").sort(byDateDesc)
  );
  eleventyConfig.addCollection("upcomingEvents", (c) => {
    const t = todayStr();
    return c
      .getFilteredByGlob("src/events/*.md")
      .filter((e) => isoDate(e.data.date) >= t)
      .sort(byDateDesc);
  });
  eleventyConfig.addCollection("pastEvents", (c) => {
    const t = todayStr();
    return c
      .getFilteredByGlob("src/events/*.md")
      .filter((e) => isoDate(e.data.date) < t)
      .sort(byDateDesc);
  });
  eleventyConfig.addCollection("artistsList", (c) =>
    c
      .getFilteredByGlob("src/artists/*.md")
      .sort((a, b) => (a.data.name || "").localeCompare(b.data.name || ""))
  );

  return {
    dir: { input: "src", output: "_site", includes: "_includes" },
  };
};
