// Import markdown parser
#import "@preview/cmarker:0.1.1": render as markdown

// Read CV data from YAML
#let data = yaml("../../data/cv.yaml")
#let info = data.info

// Page setup
#set page(margin: (x: 2.5cm, y: 2cm), numbering: none)
#set text(size: 10pt)
#set par(justify: false)

// Vertical centering
#v(1fr)

// Header
#align(center)[
  #text(size: 24pt, smallcaps(info.name))
  #v(-2.3em)
  #line(length: 100%, stroke: 0.5pt)
  #v(-0.8em)
  #text(size: 12pt)[
    *Email:* #link("mailto:" + info.email)[#raw(info.email)] #h(1fr)
    *Website:* #link("https://" + info.website)[#info.website] #h(1fr)
    *GitHub:* #link("https://" + info.github)[#info.github]
  ]
]

// Gray links for body
#show link: set text(fill: gray)

// Process sections
#for section in data.sections [
  #v(-0.25em)
  #text(size: 17pt, smallcaps(section.title))
  #v(-1.5em)
  #line(length: 100%, stroke: 0.5pt)
  #v(-1.12em)

  #table(
    columns: (0.14fr, 0.86fr),
    stroke: none,
    inset: 0pt,
    ..(
      for entry in section.entries {
        let label = entry.label
        let items = entry.items

        for (idx, item) in items.enumerate() {
          (
            // Left cell (label or empty)
            table.cell(
              align: right,
              stroke: (right: 0.5pt + luma(200)),
              inset: (left: 0pt, right: 0.6em, y: 0.6em),
              if idx == 0 { emph(str(label)) } else { [] }
            ),
            // Right cell (content)
            table.cell(
              inset: (left: 0.6em, right: 0pt, y: 0.6em),
              {
                // Convert single newlines to markdown hard breaks (two spaces + newline)
                // Don't convert \n\n to hard breaks - keep as is for tighter spacing
                let text = item.replace("\n\n", "\n")
                let text = text.replace("\n", "  \n")
                markdown(text)
              }
            ),
          )
        }
      }.flatten()
    )
  )
]

// Bottom spacing for optical balance
#v(2fr)
