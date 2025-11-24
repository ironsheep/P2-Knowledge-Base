#!/usr/bin/env node
/**
 * Doc Forge PDF Optimizer
 * Post-processes PDFs for smaller file sizes and better quality
 */

const fs = require('fs-extra');
const chalk = require('chalk');
const { execSync } = require('child_process');
const path = require('path');

async function optimizePDFs(directory = 'outbox') {
  console.log(chalk.blue('⚡ Optimizing PDFs...'));
  
  try {
    // Find all PDF files
    const files = await fs.readdir(directory);
    const pdfFiles = files.filter(file => path.extname(file) === '.pdf');
    
    if (pdfFiles.length === 0) {
      console.log(chalk.yellow('⚠ No PDF files found to optimize'));
      return true;
    }
    
    console.log(`Found ${pdfFiles.length} PDF(s) to optimize`);
    
    let optimized = 0;
    let totalSavings = 0;
    
    for (const file of pdfFiles) {
      const filePath = path.join(directory, file);
      const tempPath = path.join(directory, `${file}.temp`);
      
      console.log(chalk.gray(`  Optimizing: ${file}`));
      
      // Get original size
      const originalStats = await fs.stat(filePath);
      const originalSize = originalStats.size;
      
      try {
        // Use ghostscript for PDF optimization if available
        const gsCommand = [
          'gs',
          '-sDEVICE=pdfwrite',
          '-dCompatibilityLevel=1.4',
          '-dPDFSETTINGS=/prepress',
          '-dNOPAUSE',
          '-dQUIET',
          '-dBATCH',
          `-sOutputFile="${tempPath}"`,
          `"${filePath}"`
        ].join(' ');
        
        execSync(gsCommand, { stdio: 'pipe' });
        
        // Check if optimization was successful
        if (await fs.pathExists(tempPath)) {
          const optimizedStats = await fs.stat(tempPath);
          const optimizedSize = optimizedStats.size;
          
          // Only replace if significantly smaller (or at least not larger)
          if (optimizedSize <= originalSize) {
            await fs.move(tempPath, filePath, { overwrite: true });
            
            const savings = originalSize - optimizedSize;
            const percent = ((savings / originalSize) * 100).toFixed(1);
            
            console.log(chalk.green('✓') + ` ${file}: ${formatBytes(savings)} saved (${percent}%)`);
            optimized++;
            totalSavings += savings;
          } else {
            // Remove temp file if optimization made it larger
            await fs.remove(tempPath);
            console.log(chalk.gray('⚬') + ` ${file}: no improvement`);
          }
        }
        
      } catch (gsError) {
        // Fallback: basic cleanup without ghostscript
        console.log(chalk.yellow('⚠') + ` ${file}: ghostscript not available, skipping`);
        
        // Clean up temp file if it exists
        if (await fs.pathExists(tempPath)) {
          await fs.remove(tempPath);
        }
      }
    }
    
    console.log('');
    if (optimized > 0) {
      console.log(chalk.green('✅ Optimization complete!'));
      console.log(`Optimized ${optimized}/${pdfFiles.length} files`);
      console.log(`Total space saved: ${formatBytes(totalSavings)}`);
    } else {
      console.log(chalk.blue('ℹ All files already optimized'));
    }
    
    return true;
    
  } catch (error) {
    console.log('');
    console.log(chalk.red('❌ Optimization failed:'));
    console.log(chalk.red(`   ${error.message}`));
    return false;
  }
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// CLI usage
if (require.main === module) {
  const directory = process.argv[2] || 'outbox';
  
  optimizePDFs(directory)
    .then(success => process.exit(success ? 0 : 1))
    .catch(error => {
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    });
}

module.exports = { optimizePDFs };