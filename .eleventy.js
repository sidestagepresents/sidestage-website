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
  // "Today" in Toronto time, so tonight's show doesn't vanish at 8pm ET (midnight UTC)
  const todayStr = () => {
    const now = new Date();
    const toronto = new Date(now.getTime() + torontoOffsetMinutes(now) * 60000);
    return toronto.toISOString().slice(0, 10);
  };

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
  const byDateAsc = (a, b) => (isoDate(a.data.date) < isoDate(b.data.date) ? -1 : 1);

  // Append default UTM tags to outbound ticket links (skips params already set)
  const addUtm = (url) => {
    if (!url) return url;
    try {
      const u = new URL(url);
      if (!u.searchParams.has("utm_source")) u.searchParams.set("utm_source", "sidestagepresents.com");
      if (!u.searchParams.has("utm_medium")) u.searchParams.set("utm_medium", "referral");
      return u.toString();
    } catch {
      return url;
    }
  };
  eleventyConfig.addFilter("utm", addUtm);

  // Responsive, optimized event images: upload anything, the build serves WebP.
  // Transforms run once in eleventy.before (async); the shortcode itself stays
  // sync so it works inside Nunjucks macros. Only event/artist images are
  // transformed — the logo and favicon are served byte-identical.
  const path = require("path");
  const fs = require("fs");
  const imageHtmlCache = new Map();
  eleventyConfig.on("eleventy.before", async () => {
    const { default: Image } = await import("@11ty/eleventy-img");
    const seen = new Set();
    const readFrontMatter = (file) => {
      const text = fs.readFileSync(file, "utf8");
      const m = text.match(/^---\n([\s\S]*?)\n---/);
      if (!m) return {};
      const data = {};
      for (const line of m[1].split("\n")) {
        const kv = line.match(/^([A-Za-z_]+):\s*(.*)$/);
        if (kv) data[kv[1]] = kv[2].trim().replace(/^['"]|['"]$/g, "");
      }
      return data;
    };
    for (const dir of ["./src/events", "./src/artists"]) {
      if (!fs.existsSync(dir)) continue;
      for (const f of fs.readdirSync(dir)) {
        if (!f.endsWith(".md")) continue;
        const data = readFrontMatter(`${dir}/${f}`);
        const src = data.image;
        if (!src || seen.has(src)) continue;
        seen.add(src);
        const alt = data.artist ? `${data.artist} flyer` : data.name || "";
        try {
          const metadata = await Image("./src" + src, {
            widths: [400, 800],
            formats: ["webp", "jpeg"],
            outputDir: "./_site/img/",
            urlPath: "/img/",
            filenameFormat: (id, srcPath, width, format) =>
              `${path.parse(srcPath).name}-${width}w.${format}`,
          });
          imageHtmlCache.set(
            src,
            Image.generateHTML(metadata, {
              alt,
              loading: "lazy",
              decoding: "async",
              sizes: "(max-width: 600px) 100vw, 200px",
            })
          );
        } catch {
          /* fall back to the plain img tag below */
        }
      }
    }
  });
  eleventyConfig.addNunjucksShortcode("eventImage", (src, alt) => {
    return (
      imageHtmlCache.get(src) ||
      `<img src="${src}" alt="${alt || ""}" loading="lazy">`
    );
  });

  eleventyConfig.addCollection("allEvents", (c) =>
    notDraft(c.getFilteredByGlob("src/events/*.md")).sort(byDateDesc)
  );
  eleventyConfig.addCollection("upcomingEvents", (c) => {
    const t = todayStr();
    return notDraft(c.getFilteredByGlob("src/events/*.md"))
      .filter((e) => isoDate(e.data.date) >= t)
      .sort(byDateAsc);
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
