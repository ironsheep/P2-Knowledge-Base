#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fs from 'fs';
import path from 'path';
import yaml from 'yaml';
import { glob } from 'glob';

// Find the knowledge base root
const KB_ROOT = process.env.P2KB_PATH || path.resolve(process.cwd());
const PASM2_PATH = path.join(KB_ROOT, 'engineering/knowledge-base/P2/language/pasm2');
const SPIN2_PATH = path.join(KB_ROOT, 'engineering/knowledge-base/P2/language/spin2');
const SMARTPINS_PATH = path.join(KB_ROOT, 'engineering/knowledge-base/P2/hardware/smart-pins/modes');
const MANIFESTS_PATH = path.join(KB_ROOT, 'manifests');

class P2KnowledgeBaseServer {
  constructor() {
    this.server = new Server(
      {
        name: 'p2-knowledge-base',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  async loadYamlFile(filePath) {
    try {
      const content = await fs.promises.readFile(filePath, 'utf8');
      return yaml.parse(content);
    } catch (error) {
      return null;
    }
  }

  async loadManifest(manifestName) {
    const manifestPath = path.join(MANIFESTS_PATH, manifestName);
    return this.loadYamlFile(manifestPath);
  }

  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'p2_instruction',
          description: 'Look up a P2 PASM2 instruction by mnemonic',
          inputSchema: {
            type: 'object',
            properties: {
              mnemonic: {
                type: 'string',
                description: 'Instruction mnemonic (e.g., ADD, MOV, JMP)',
              },
              category: {
                type: 'string',
                description: 'Optional category to narrow search',
              },
            },
            required: ['mnemonic'],
          },
        },
        {
          name: 'p2_instruction_list',
          description: 'List all P2 instructions in a category',
          inputSchema: {
            type: 'object',
            properties: {
              category: {
                type: 'string',
                description: 'Category name (e.g., math, flow, memory)',
              },
            },
            required: ['category'],
          },
        },
        {
          name: 'smart_pin_mode',
          description: 'Get Smart Pin mode configuration',
          inputSchema: {
            type: 'object',
            properties: {
              mode: {
                type: 'string',
                description: 'Mode number or binary (e.g., 00010 or sync_tx)',
              },
            },
            required: ['mode'],
          },
        },
        {
          name: 'smart_pin_list',
          description: 'List all available Smart Pin modes',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'spin2_method',
          description: 'Look up a Spin2 method',
          inputSchema: {
            type: 'object',
            properties: {
              method: {
                type: 'string',
                description: 'Method name (e.g., cogid, waitms)',
              },
            },
            required: ['method'],
          },
        },
        {
          name: 'search_patterns',
          description: 'Search for code patterns',
          inputSchema: {
            type: 'object',
            properties: {
              pattern: {
                type: 'string',
                description: 'Pattern to search for (e.g., multi-cog, pwm, spi)',
              },
            },
            required: ['pattern'],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'p2_instruction':
          return this.lookupInstruction(args.mnemonic, args.category);

        case 'p2_instruction_list':
          return this.listInstructions(args.category);

        case 'smart_pin_mode':
          return this.getSmartPinMode(args.mode);

        case 'smart_pin_list':
          return this.listSmartPinModes();

        case 'spin2_method':
          return this.lookupSpin2Method(args.method);

        case 'search_patterns':
          return this.searchPatterns(args.pattern);

        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  async lookupInstruction(mnemonic, category) {
    try {
      // First try to find in specific category if provided
      if (category) {
        const categoryPath = path.join(PASM2_PATH, category);
        const files = await glob(`${categoryPath}/${mnemonic.toLowerCase()}.yaml`);
        if (files.length > 0) {
          const data = await this.loadYamlFile(files[0]);
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify(data, null, 2),
              },
            ],
          };
        }
      }

      // Search all categories
      const files = await glob(`${PASM2_PATH}/**/${mnemonic.toLowerCase()}.yaml`);
      if (files.length > 0) {
        const data = await this.loadYamlFile(files[0]);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      return {
        content: [
          {
            type: 'text',
            text: `Instruction '${mnemonic}' not found`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `Error: ${error.message}`,
          },
        ],
      };
    }
  }

  async listInstructions(category) {
    try {
      const manifest = await this.loadManifest('pasm2-manifest.yaml');
      if (!manifest || !manifest.categories) {
        throw new Error('Could not load PASM2 manifest');
      }

      const categoryData = manifest.categories.find(c => 
        c.name.toLowerCase() === category.toLowerCase() ||
        c.path === category
      );

      if (!categoryData) {
        return {
          content: [
            {
              type: 'text',
              text: `Category '${category}' not found. Available categories: ${
                manifest.categories.map(c => c.name).join(', ')
              }`,
            },
          ],
        };
      }

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              category: categoryData.name,
              description: categoryData.description,
              instructions: categoryData.instructions,
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `Error: ${error.message}`,
          },
        ],
      };
    }
  }

  async getSmartPinMode(mode) {
    try {
      // Handle different mode formats
      let searchPattern;
      if (mode.match(/^\d{5}$/)) {
        // Binary format: 00010
        searchPattern = `${mode}_*.yaml`;
      } else if (mode.match(/^\d+$/)) {
        // Decimal format: convert to binary
        const binary = parseInt(mode).toString(2).padStart(5, '0');
        searchPattern = `${binary}_*.yaml`;
      } else {
        // Name format: sync_tx
        searchPattern = `*_${mode}.yaml`;
      }

      const files = await glob(path.join(SMARTPINS_PATH, searchPattern));
      if (files.length > 0) {
        const data = await this.loadYamlFile(files[0]);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      return {
        content: [
          {
            type: 'text',
            text: `Smart Pin mode '${mode}' not found`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `Error: ${error.message}`,
          },
        ],
      };
    }
  }

  async listSmartPinModes() {
    try {
      const files = await glob(path.join(SMARTPINS_PATH, '*.yaml'));
      const modes = [];

      for (const file of files) {
        const basename = path.basename(file, '.yaml');
        const parts = basename.split('_');
        const binary = parts[0];
        const name = parts.slice(1).join('_');
        
        const data = await this.loadYamlFile(file);
        modes.push({
          binary,
          decimal: parseInt(binary, 2),
          name,
          description: data?.description || '',
        });
      }

      modes.sort((a, b) => a.decimal - b.decimal);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(modes, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `Error: ${error.message}`,
          },
        ],
      };
    }
  }

  async lookupSpin2Method(method) {
    try {
      const methodFile = path.join(SPIN2_PATH, 'methods', `${method.toLowerCase()}.yaml`);
      const data = await this.loadYamlFile(methodFile);
      
      if (data) {
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      return {
        content: [
          {
            type: 'text',
            text: `Spin2 method '${method}' not found`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `Error: ${error.message}`,
          },
        ],
      };
    }
  }

  async searchPatterns(pattern) {
    try {
      const patternFiles = await glob(
        path.join(KB_ROOT, 'engineering/ingestion/external-inputs/source-code/external-projects', 
                  '*', `*${pattern}*.md`)
      );

      const results = [];
      for (const file of patternFiles) {
        const content = await fs.promises.readFile(file, 'utf8');
        const lines = content.split('\n');
        const matches = lines.filter(line => 
          line.toLowerCase().includes(pattern.toLowerCase())
        );
        
        if (matches.length > 0) {
          results.push({
            file: path.relative(KB_ROOT, file),
            matches: matches.slice(0, 5), // First 5 matches
          });
        }
      }

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(results, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `Error: ${error.message}`,
          },
        ],
      };
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('P2 Knowledge Base MCP server running');
  }
}

const server = new P2KnowledgeBaseServer();
server.run().catch(console.error);