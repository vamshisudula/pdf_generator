"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PDFGenerator = void 0;
const puppeteer_1 = __importDefault(require("puppeteer"));
const ejs_1 = __importDefault(require("ejs"));
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
class PDFGenerator {
    constructor() {
        // Use the directory where the compiled JS file is located
        this.templatesDir = path_1.default.join(__dirname);
        this.outputDir = path_1.default.join(__dirname, 'output');
        // Create output directory if it doesn't exist
        if (!fs_1.default.existsSync(this.outputDir)) {
            fs_1.default.mkdirSync(this.outputDir);
        }
        // Verify template files exist
        const requiredFiles = [
            '3_market_outlook.html',
            '4_debt_overview.html',
            '5_asset_allocation.html',
            'globals.css',
            'style.css',
            'mutual_fund_style.css'
        ];
        for (const file of requiredFiles) {
            const filePath = path_1.default.join(this.templatesDir, file);
            if (!fs_1.default.existsSync(filePath)) {
                throw new Error(`Required template file not found: ${file}`);
            }
        }
    }
    async generatePage(templatePath, data) {
        try {
            const template = fs_1.default.readFileSync(templatePath, 'utf-8');
            return ejs_1.default.render(template, data);
        }
        catch (error) {
            console.error(`Error reading template ${templatePath}:`, error);
            throw error;
        }
    }
    async generatePDF(html, outputPath) {
        const browser = await puppeteer_1.default.launch({
            headless: 'new',
            args: ['--no-sandbox']
        });
        try {
            const page = await browser.newPage();
            // Set content and wait for network to be idle
            await page.setContent(html, {
                waitUntil: 'networkidle0'
            });
            // Wait for any images to load
            await page.evaluate(() => {
                return Promise.all(Array.from(document.images)
                    .filter(img => !img.complete)
                    .map(img => new Promise(resolve => {
                    img.onload = img.onerror = resolve;
                })));
            });
            await page.pdf({
                path: outputPath,
                format: 'A4',
                printBackground: true,
                margin: {
                    top: '20px',
                    right: '20px',
                    bottom: '20px',
                    left: '20px'
                }
            });
        }
        catch (error) {
            console.error('Error generating PDF:', error);
            throw error;
        }
        finally {
            await browser.close();
        }
    }
    async generateMarketOutlook(marketOutlookData) {
        const templatePath = path_1.default.join(this.templatesDir, '3_market_outlook.html');
        const outputPath = path_1.default.join(this.outputDir, 'market_outlook.pdf');
        const html = await this.generatePage(templatePath, {
            textareaContent: marketOutlookData.marketOutlook
        });
        await this.generatePDF(html, outputPath);
        return outputPath;
    }
    async generateDebtOverview(marketOutlookData) {
        const templatePath = path_1.default.join(this.templatesDir, '4_debt_overview.html');
        const outputPath = path_1.default.join(this.outputDir, 'debt_overview.pdf');
        const html = await this.generatePage(templatePath, {
            textareaContent: marketOutlookData.description
        });
        await this.generatePDF(html, outputPath);
        return outputPath;
    }
    async generateAssetAllocation(assetAllocationData) {
        const templatePath = path_1.default.join(this.templatesDir, '5_asset_allocation.html');
        const outputPath = path_1.default.join(this.outputDir, 'asset_allocation.pdf');
        // Calculate total amount for each asset class
        const assetClassAmounts = Object.entries(assetAllocationData.assetClassAllocation).map(([asset, percentage]) => ({
            asset,
            percentage,
            amount: (assetAllocationData.portfolioSize * percentage) / 100
        }));
        const html = await this.generatePage(templatePath, {
            portfolioSize: assetAllocationData.portfolioSize,
            assetClassAmounts,
            rationale: assetAllocationData.rationale
        });
        await this.generatePDF(html, outputPath);
        return outputPath;
    }
    async generateFullProposal(marketOutlookData, assetAllocationData) {
        const pdfPaths = await Promise.all([
            this.generateMarketOutlook(marketOutlookData),
            this.generateDebtOverview(marketOutlookData),
            this.generateAssetAllocation(assetAllocationData)
        ]);
        return pdfPaths;
    }
}
exports.PDFGenerator = PDFGenerator;
