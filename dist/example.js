"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const pdfGenerator_1 = require("./pdfGenerator");
async function main() {
    const pdfGenerator = new pdfGenerator_1.PDFGenerator();
    // Example market outlook data
    const marketOutlookData = {
        marketOutlook: "The Indian equity market has shown resilience despite global headwinds. Key sectors like IT, Banking, and Infrastructure continue to show strong growth potential. We expect the market to maintain its upward trajectory in the medium term.",
        description: "The debt market remains stable with RBI maintaining its accommodative stance. Corporate bond yields have moderated, presenting good opportunities for fixed income investments. We recommend a balanced approach with focus on high-quality corporate bonds and government securities."
    };
    // Example asset allocation data
    const assetAllocationData = {
        portfolioSize: 25000000, // 2.5 Cr
        assetClassAllocation: {
            equity: 60,
            debt: 30,
            gold: 10
        },
        rationale: "The allocation is based on the client's risk profile and investment objectives. Higher equity allocation is recommended for long-term wealth creation, while debt provides stability and regular income. Gold allocation helps in portfolio diversification and acts as a hedge against inflation."
    };
    try {
        // Generate individual PDFs
        const marketOutlookPath = await pdfGenerator.generateMarketOutlook(marketOutlookData);
        console.log('Market Outlook PDF generated:', marketOutlookPath);
        const debtOverviewPath = await pdfGenerator.generateDebtOverview(marketOutlookData);
        console.log('Debt Overview PDF generated:', debtOverviewPath);
        const assetAllocationPath = await pdfGenerator.generateAssetAllocation(assetAllocationData);
        console.log('Asset Allocation PDF generated:', assetAllocationPath);
        // Or generate all PDFs at once
        const allPdfPaths = await pdfGenerator.generateFullProposal(marketOutlookData, assetAllocationData);
        console.log('All PDFs generated:', allPdfPaths);
    }
    catch (error) {
        console.error('Error generating PDFs:', error);
    }
}
main().catch(console.error);
