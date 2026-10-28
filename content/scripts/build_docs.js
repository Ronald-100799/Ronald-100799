// Build one Word document per week from weeks.json (made by merge_meta.py).
// Usage: node build_docs.js weeks.json outDir
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, AlignmentType, LevelFormat, Footer, PageNumber, ExternalHyperlink,
} = require("docx");

const [, , inFile, outDir] = process.argv;
const weeks = JSON.parse(fs.readFileSync(inFile, "utf8"));
fs.mkdirSync(outDir, { recursive: true });

const YELLOW = "FFE11A", INK = "1F1F1F", GREY = "6B6B6B", SOFT = "FFF7C2", LINE = "D9D9D9";
const CONTENT_W = 9026; // A4 with 1" margins, in DXA
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const fmtDate = (iso) => { const [y, m, d] = iso.split("-").map(Number); return `${d} ${MONTHS[m - 1]}`; };

const border = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const borders = { top: border, bottom: border, left: border, right: border };
const cell = (text, w, opts = {}) => new TableCell({
  borders, width: { size: w, type: WidthType.DXA },
  shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
  margins: { top: 60, bottom: 60, left: 100, right: 100 },
  children: [new Paragraph({ children: Array.isArray(text) ? text : [new TextRun({ text: String(text), bold: !!opts.bold, size: opts.size || 20 })] })],
});

function infoTable(it) {
  const W = [2200, CONTENT_W - 2200];
  const link = (u) => u ? [new ExternalHyperlink({ link: u, children: [new TextRun({ text: u, style: "Hyperlink", size: 18 })] })] : [];
  const srcRuns = [new TextRun({ text: it.source, size: 20 }), new TextRun({ text: "  ", size: 20 }), ...link(it.url)];
  if (it.url2) srcRuns.push(new TextRun({ text: "   Also: ", size: 18, color: GREY }), ...link(it.url2));
  const rows = [
    ["Pillar / type", it.type],
    ["Goal", it.goal],
    ["Estimated length", `~${it.secs} s spoken in English (${it.words} words). Keep the Tamil delivery under 90 s.`],
    ["Source to show", srcRuns],
  ];
  if (it.link) rows.push(["Link test", [new TextRun({ text: `Comment "${it.link[0]}" → DM the doc: `, bold: true, size: 20 }), new TextRun({ text: it.link[1], size: 20 })]]);
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: W,
    rows: rows.map(([k, v]) => new TableRow({ children: [cell(k, W[0], { bold: true, fill: SOFT }), cell(v, W[1])] })),
  });
}

function sectionBlock(sec) {
  const out = [new Paragraph({
    spacing: { before: 110, after: 40 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: YELLOW, space: 1 } },
    children: [
      new TextRun({ text: `${sec.time}  `, bold: true, color: GREY, size: 20 }),
      new TextRun({ text: sec.label, bold: true, size: 22 }),
      ...(sec.fast ? [new TextRun({ text: "   FAST: cut every 1–2 s", bold: true, color: "B54708", size: 18 })] : []),
    ],
  })];
  for (const [typ, text] of sec.lines) {
    if (typ === "S") {
      out.push(new Paragraph({ spacing: { after: 40 }, indent: { left: 240 }, children: [new TextRun({ text, size: 22 })] }));
    } else {
      out.push(new Paragraph({ spacing: { after: 40 }, indent: { left: 240 }, children: [new TextRun({ text: `[${text}]`, italics: true, color: GREY, size: 18 })] }));
    }
  }
  return out;
}

const bullet = (runs) => new Paragraph({ numbering: { reference: "dots", level: 0 }, spacing: { after: 60 },
  children: typeof runs === "string" ? [new TextRun({ text: runs, size: 21 })] : runs });

function intro(weekStart, items) {
  const end = new Date(weekStart); end.setDate(end.getDate() + 6);
  const endIso = end.toISOString().slice(0, 10);
  const W = [1500, 800, 1300, 3426, 900, 1100];
  const head = ["Day", "ID", "Format", "Topic", "Length", "Link test"];
  return [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun({ text: `Reel scripts: ${fmtDate(weekStart)} – ${fmtDate(endIso)} 2026` })] }),
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "@ron_tamil · 7 reels · v2 (7-beat structure) · English drafts. Say them your way in Tamil/Thanglish.", color: GREY, size: 22 })] }),
    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("This week")] }),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: W,
      rows: [new TableRow({ tableHeader: true, children: head.map((h, i) => cell(h, W[i], { bold: true, fill: YELLOW })) }),
        ...items.map((it) => new TableRow({ children: [
          cell(`${it.day} ${fmtDate(it.date)}`, W[0]), cell(it.id, W[1]), cell(it.format, W[2]), cell(it.topic, W[3]),
          cell(`~${it.secs} s`, W[4]), cell(it.link ? it.link[0] : "–", W[5])] }))],
    }),
    new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 300 }, children: [new TextRun("The 7-beat structure (v2)")] }),
    bullet([new TextRun({ text: "1 Hook (0–6 s): ", bold: true, size: 21 }), new TextRun({ text: "curiosity in the first 3 s (a number, a price, a known claim), then a pattern interrupt that says the opposite of what they expect. The rising SFX runs under the curiosity line and the movie meme lands on the turn.", size: 21 })]),
    bullet([new TextRun({ text: "2 Value by 13 s: ", bold: true, size: 21 }), new TextRun({ text: "one real fact with the research on screen, so the reel feels high-value early. The authority line is folded in here.", size: 21 })]),
    bullet([new TextRun({ text: "3 First problem: ", bold: true, size: 21 }), new TextRun({ text: "even with that fact, they still can't act. This re-hooks them.", size: 21 })]),
    bullet([new TextRun({ text: "4 False relief: ", bold: true, size: 21 }), new TextRun({ text: "half the fix: a small win, but not the full answer.", size: 21 })]),
    bullet([new TextRun({ text: "5 Second, bigger problem: ", bold: true, size: 21 }), new TextRun({ text: "the loop re-opens, which keeps people watching.", size: 21 })]),
    bullet([new TextRun({ text: "6 Solution (~40–55 s): ", bold: true, size: 21 }), new TextRun({ text: "answers everything at once. Save prompts and link tests sit here.", size: 21 })]),
    bullet([new TextRun({ text: "7 Emotional CTA: ", bold: true, size: 21 }), new TextRun({ text: "ends on hope, then a soft share ask that names who to send it to. Shares carry a reel to non-followers.", size: 21 })]),
    bullet([new TextRun({ text: "What changed from v1: ", bold: true, size: 21 }), new TextRun({ text: "value now lands by 13 s (v1 often reached it at 14–20 s, after a separate authority line); every script now has two problems and a false relief instead of answering the myth straight away; endings lead with hope instead of a hard ask. Facts and sources are unchanged.", size: 21 })]),
    bullet([new TextRun({ text: "Link test: ", bold: true, size: 21 }), new TextRun({ text: "teaching reels include \"Comment KEYWORD and I'll send you the doc\" in the solution beat. Ask Claude to write the docs.", size: 21 })]),
    bullet([new TextRun({ text: "Reading the scripts: ", bold: true, size: 21 }), new TextRun({ text: "plain text is spoken; [grey italics] are edit directions. Lines starting CHECK must be confirmed before filming. Timings are targets; keep every reel under 90 s in Tamil.", size: 21 })]),
  ];
}

for (const [weekStart, items] of Object.entries(weeks).sort()) {
  const children = intro(weekStart, items);
  for (const it of items) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun(`${it.id} · ${it.day} ${fmtDate(it.date)} · ${it.format}`)] }));
    children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: it.topic, bold: true, size: 30 })] }));
    children.push(infoTable(it));
    for (const sec of it.sections) children.push(...sectionBlock(sec));
  }
  const doc = new Document({
    creator: "Claude for @ron_tamil", title: `Reel scripts ${weekStart}`,
    styles: {
      default: { document: { run: { font: "Arial", size: 22, color: INK } } },
      paragraphStyles: [
        { id: "Title", name: "Title", basedOn: "Normal", run: { size: 40, bold: true, font: "Arial" }, paragraph: { spacing: { after: 80 } } },
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Arial", color: GREY }, paragraph: { spacing: { before: 0, after: 60 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Arial" }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
      ],
    },
    numbering: { config: [{ reference: "dots", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
    sections: [{
      properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
        new TextRun({ text: "@ron_tamil reel scripts · page ", color: GREY, size: 16 }), new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 16 })] })] }) },
      children,
    }],
  });
  const end = new Date(weekStart); end.setDate(end.getDate() + 6);
  const name = `Reel-Scripts_${weekStart}_to_${end.toISOString().slice(0, 10)}.docx`;
  Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(path.join(outDir, name), buf); console.log("wrote", name, buf.length); });
}
