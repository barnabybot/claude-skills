#!/usr/bin/env node
/**
 * Create a professional Word document with docx-js.
 * 
 * This example demonstrates:
 * - Document creation with metadata
 * - Headings and paragraphs
 * - Bullet lists and numbered lists
 * - Tables with formatting
 * - Bold, italic, and other text formatting
 * 
 * Usage:
 *   node create_document.js
 *   node create_document.js output.docx
 * 
 * Dependencies:
 *   npm install docx
 */

const { Document, Packer, Paragraph, TextRun, HeadingLevel, 
        Table, TableRow, TableCell, WidthType, BorderStyle,
        AlignmentType, NumberFormat } = require("docx");
const fs = require("fs");

async function createDocument(outputPath = "example_document.docx") {
    
    const doc = new Document({
        creator: "DOCX Skill Example",
        title: "Project Status Report",
        description: "Example document created with docx-js",
        sections: [{
            properties: {},
            children: [
                // Title
                new Paragraph({
                    text: "Project Status Report",
                    heading: HeadingLevel.HEADING_1,
                    spacing: { after: 200 }
                }),
                
                // Subtitle/date
                new Paragraph({
                    children: [
                        new TextRun({
                            text: "Prepared: January 2026",
                            italics: true,
                            color: "666666"
                        })
                    ],
                    spacing: { after: 400 }
                }),
                
                // Executive Summary heading
                new Paragraph({
                    text: "Executive Summary",
                    heading: HeadingLevel.HEADING_2,
                    spacing: { before: 200, after: 100 }
                }),
                
                // Summary paragraph
                new Paragraph({
                    children: [
                        new TextRun("The project is "),
                        new TextRun({
                            text: "on track",
                            bold: true
                        }),
                        new TextRun(" for completion by the target date. Key milestones have been achieved, and the team has addressed all critical blockers identified in the previous review.")
                    ],
                    spacing: { after: 200 }
                }),
                
                // Key Highlights heading
                new Paragraph({
                    text: "Key Highlights",
                    heading: HeadingLevel.HEADING_2,
                    spacing: { before: 200, after: 100 }
                }),
                
                // Bullet list
                new Paragraph({
                    text: "Phase 1 development completed ahead of schedule",
                    bullet: { level: 0 }
                }),
                new Paragraph({
                    text: "User acceptance testing passed with 98% success rate",
                    bullet: { level: 0 }
                }),
                new Paragraph({
                    text: "Technical documentation finalized",
                    bullet: { level: 1 }
                }),
                new Paragraph({
                    text: "Training materials prepared",
                    bullet: { level: 1 }
                }),
                new Paragraph({
                    text: "Budget utilization at 87% of allocated funds",
                    bullet: { level: 0 },
                    spacing: { after: 200 }
                }),
                
                // Metrics heading
                new Paragraph({
                    text: "Project Metrics",
                    heading: HeadingLevel.HEADING_2,
                    spacing: { before: 200, after: 100 }
                }),
                
                // Table
                new Table({
                    width: { size: 100, type: WidthType.PERCENTAGE },
                    rows: [
                        // Header row
                        new TableRow({
                            children: [
                                new TableCell({
                                    children: [new Paragraph({ 
                                        text: "Metric",
                                        alignment: AlignmentType.CENTER
                                    })],
                                    shading: { fill: "DDDDDD" }
                                }),
                                new TableCell({
                                    children: [new Paragraph({ 
                                        text: "Target",
                                        alignment: AlignmentType.CENTER
                                    })],
                                    shading: { fill: "DDDDDD" }
                                }),
                                new TableCell({
                                    children: [new Paragraph({ 
                                        text: "Actual",
                                        alignment: AlignmentType.CENTER
                                    })],
                                    shading: { fill: "DDDDDD" }
                                }),
                                new TableCell({
                                    children: [new Paragraph({ 
                                        text: "Status",
                                        alignment: AlignmentType.CENTER
                                    })],
                                    shading: { fill: "DDDDDD" }
                                })
                            ]
                        }),
                        // Data rows
                        new TableRow({
                            children: [
                                new TableCell({ children: [new Paragraph("Timeline")] }),
                                new TableCell({ children: [new Paragraph("12 weeks")] }),
                                new TableCell({ children: [new Paragraph("11 weeks")] }),
                                new TableCell({ children: [new Paragraph("✓ Ahead")] })
                            ]
                        }),
                        new TableRow({
                            children: [
                                new TableCell({ children: [new Paragraph("Budget")] }),
                                new TableCell({ children: [new Paragraph("$500K")] }),
                                new TableCell({ children: [new Paragraph("$435K")] }),
                                new TableCell({ children: [new Paragraph("✓ Under")] })
                            ]
                        }),
                        new TableRow({
                            children: [
                                new TableCell({ children: [new Paragraph("Quality")] }),
                                new TableCell({ children: [new Paragraph("95%")] }),
                                new TableCell({ children: [new Paragraph("98%")] }),
                                new TableCell({ children: [new Paragraph("✓ Exceeded")] })
                            ]
                        })
                    ]
                }),
                
                // Next Steps
                new Paragraph({
                    text: "Next Steps",
                    heading: HeadingLevel.HEADING_2,
                    spacing: { before: 400, after: 100 }
                }),
                
                // Numbered list
                new Paragraph({
                    text: "Complete final integration testing",
                    numbering: { reference: "numbered-list", level: 0 }
                }),
                new Paragraph({
                    text: "Conduct stakeholder review session",
                    numbering: { reference: "numbered-list", level: 0 }
                }),
                new Paragraph({
                    text: "Deploy to production environment",
                    numbering: { reference: "numbered-list", level: 0 }
                }),
                new Paragraph({
                    text: "Begin post-launch monitoring",
                    numbering: { reference: "numbered-list", level: 0 }
                })
            ]
        }],
        numbering: {
            config: [{
                reference: "numbered-list",
                levels: [{
                    level: 0,
                    format: NumberFormat.DECIMAL,
                    text: "%1.",
                    alignment: AlignmentType.START
                }]
            }]
        }
    });
    
    // Generate and save
    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(outputPath, buffer);
    
    console.log(`Created: ${outputPath}`);
}

// Run
const outputPath = process.argv[2] || "example_document.docx";
createDocument(outputPath).catch(console.error);
