const pptxgen = require('pptxgenjs');
const html2pptx = require('/Users/fabswill/.claude/skills/document-skills/pptx/scripts/html2pptx.js');
const path = require('path');

async function createPresentation() {
    console.log('Creating MCP Presentation...\n');

    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Fabian Williams';
    pptx.title = 'Getting Started with Model Context Protocol (MCP)';
    pptx.subject = 'TechCon365 Dallas 2025';

    const slidesDir = path.join(__dirname, 'slides');

    // Slide 1: Title
    console.log('Processing Slide 1: Title...');
    await html2pptx(path.join(slidesDir, 'slide01-title.html'), pptx);

    // Slide 2: The Problem
    console.log('Processing Slide 2: The Problem...');
    await html2pptx(path.join(slidesDir, 'slide02-problem.html'), pptx);

    // Slide 3: What is MCP
    console.log('Processing Slide 3: What is MCP...');
    await html2pptx(path.join(slidesDir, 'slide03-what-is-mcp.html'), pptx);

    // Slide 4: Local AI Advantage
    console.log('Processing Slide 4: Local AI Advantage...');
    await html2pptx(path.join(slidesDir, 'slide04-local-ai.html'), pptx);

    // Slide 5: What Stays Local
    console.log('Processing Slide 5: What Stays Local vs What Travels...');
    await html2pptx(path.join(slidesDir, 'slide05-what-stays-local.html'), pptx);

    // Slide 6: Demo 1 Intro
    console.log('Processing Slide 6: Demo #1 Intro...');
    await html2pptx(path.join(slidesDir, 'slide06-demo1-intro.html'), pptx);

    // Slide 7: Demo 1 Results
    console.log('Processing Slide 7: Demo #1 Results...');
    await html2pptx(path.join(slidesDir, 'slide07-demo1-results.html'), pptx);

    // Slide 8: Demo 2 Intro
    console.log('Processing Slide 8: Demo #2 Intro...');
    await html2pptx(path.join(slidesDir, 'slide08-demo2-intro.html'), pptx);

    // Slide 9: MCP Composition
    console.log('Processing Slide 9: MCP Composition...');
    await html2pptx(path.join(slidesDir, 'slide09-mcp-composition.html'), pptx);

    // Slide 10: Privacy Benefits
    console.log('Processing Slide 10: Privacy Benefits...');
    await html2pptx(path.join(slidesDir, 'slide10-privacy-benefits.html'), pptx);

    // Slide 11: Cost Benefits with Chart
    console.log('Processing Slide 11: Cost Benefits...');
    const { slide: slide11, placeholders } = await html2pptx(path.join(slidesDir, 'slide11-cost-benefits.html'), pptx);

    // Add cost comparison chart
    if (placeholders.length > 0) {
        const chartData = [
            {
                name: 'Cloud AI (Monthly)',
                labels: ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'],
                values: [1500, 3000, 4500, 6000, 7500, 9000]
            },
            {
                name: 'Local AI (One-time + Ongoing)',
                labels: ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'],
                values: [3500, 3550, 3600, 3650, 3700, 3750]
            }
        ];

        slide11.addChart(pptx.charts.LINE, chartData, {
            ...placeholders[0],
            showTitle: true,
            title: 'Cost Comparison: Cloud vs Local AI',
            lineSize: 4,
            lineSmooth: true,
            showCatAxisTitle: true,
            catAxisTitle: 'Time Period',
            showValAxisTitle: true,
            valAxisTitle: 'Total Cost ($)',
            valAxisMinVal: 0,
            valAxisMaxVal: 10000,
            valAxisMajorUnit: 2000,
            chartColors: ['FE4447', '40695B']
        });
    }

    // Slide 12: MCP vs Others
    console.log('Processing Slide 12: MCP vs A2A vs ACP...');
    await html2pptx(path.join(slidesDir, 'slide12-mcp-vs-others.html'), pptx);

    // Slide 13: Getting Started
    console.log('Processing Slide 13: Getting Started...');
    await html2pptx(path.join(slidesDir, 'slide13-getting-started.html'), pptx);

    // Slide 14: Resources
    console.log('Processing Slide 14: Resources...');
    await html2pptx(path.join(slidesDir, 'slide14-resources.html'), pptx);

    // Slide 15: Q&A
    console.log('Processing Slide 15: Q&A...');
    await html2pptx(path.join(slidesDir, 'slide15-qanda.html'), pptx);

    // Save presentation
    const outputPath = path.join(__dirname, 'TechCon365-MCP-Presentation.pptx');
    console.log('\nSaving presentation...');
    await pptx.writeFile({ fileName: outputPath });

    console.log(`\n✅ Presentation created successfully!`);
    console.log(`📁 Output: ${outputPath}`);
    console.log(`📊 Total slides: 15\n`);
}

createPresentation().catch(error => {
    console.error('Error creating presentation:', error);
    process.exit(1);
});
