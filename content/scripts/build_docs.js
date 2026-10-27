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
    spacing: { before: 200, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: YELLOW, space: 1 } },
    children: [
      new TextRun({ text: `${sec.time}  `, bold: true, color: GREY, size: 20 }),
      new TextRun({ text: sec.label, bold: true, size: 22 }),
      ...(sec.fast ? [new TextRun({ text: "   FAST: cut every 1–2 s", bold: true, color: "B54708", size: 18 })] : []),
    ],
  })];
  for (const [typ, text] of sec.lines) {
    if (typ === "S") {
      out.push(new Paragraph({ spacing: { after: 80 }, indent: { left: 240 }, children: [new TextRun({ text, size: 24 })] }));
    } else {
      out.push(new Paragraph({ spacing: { after: 80 }, indent: { left: 240 }, children: [new TextRun({ text: `[${text}]`, italics: true, color: GREY, size: 19 })] }));
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
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "@ron_tamil · 7 reels · English drafts. Say them your way in Tamil/Thanglish.", color: GREY, size: 22 })] }),
    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("This week")] }),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: W,
      rows: [new TableRow({ tableHeader: true, children: head.map((h, i) => cell(h, W[i], { bold: true, fill: YELLOW })) }),
        ...items.map((it) => new TableRow({ children: [
          cell(`${it.day} ${fmtDate(it.date)}`, W[0]), cell(it.id, W[1]), cell(it.format, W[2]), cell(it.topic, W[3]),
          cell(`~${it.secs} s`, W[4]), cell(it.link ? it.link[0] : "–", W[5])] }))],
    }),
    new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 300 }, children: [new TextRun("How every script is built")] }),
    bullet([new TextRun({ text: "Hook stack (0–5 s): ", bold: true, size: 21 }), new TextRun({ text: "three short hooks over a rising sound effect, then a 2-second movie meme. The first seconds decide watch time, which Instagram treats as its top signal.", size: 21 })]),
    bullet([new TextRun({ text: "Authority (by ~12 s): ", bold: true, size: 21 }), new TextRun({ text: "one line on your 8 years of training and that you read the research, so viewers trust what comes next.", size: 21 })]),
    bullet([new TextRun({ text: "Deny the obvious: ", bold: true, size: 21 }), new TextRun({ text: "each script has a \"So … ? No.\" turn, like your best-performing beginner reel, to keep people guessing.", size: 21 })]),
    bullet([new TextRun({ text: "Research on screen: ", bold: true, size: 21 }), new TextRun({ text: "every study line has an [ON-SCREEN] citation. All numbers come from the checked source in the calendar.", size: 21 })]),
    bullet([new TextRun({ text: "Follow / save CTA: ", bold: true, size: 21 }), new TextRun({ text: "a reason to follow (series, weekly study breakdowns, myths busted) or to save (lists, numbers).", size: 21 })]),
    bullet([new TextRun({ text: "Share CTA with a reason (last 20–30 s): ", bold: true, size: 21 }), new TextRun({ text: "names who to send it to and why. Sends per reach is the signal that carries a reel to non-followers.", size: 21 })]),
    bullet([new TextRun({ text: "Link test: ", bold: true, size: 21 }), new TextRun({ text: "teaching reels end with \"Comment KEYWORD and I'll send you the doc\". Reply by DM yourself or with an auto-DM tool; ask Claude to write the docs.", size: 21 })]),
    bullet([new TextRun({ text: "Reading the scripts: ", bold: true, size: 21 }), new TextRun({ text: "plain text is spoken; [grey italics] are directions for the edit. Lines starting CHECK must be confirmed before filming.", size: 21 })]),
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
