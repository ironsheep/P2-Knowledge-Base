# Auxiliary Guides Quick Reference for Remote Claude

## 🎯 When to Use Each Guide

### User Mentions → Guide to Use

| Keywords | Guide | Key Action |
|----------|-------|------------|
| "driver", "sensor", "I2C", "SPI", "serial" | `search-strategies/obex-search-optimization.md` | Search ALL 113 objects, expand keywords |
| "debug", "Plot window", "visualization", "BMP" | `special-techniques/bmp-generation-guide.md` | Generate layered BMPs with Python/Pillow |
| "test", "hardware", "download", "PropPlug" | `special-techniques/hardware-testing-guide.md` | Use pnut_ts -d, monitor logs/*.log |
| "how to use AI", "Claude", "prompts" | `interaction/using-with-ai.md` | Start with root manifest navigation |

## 🔴 Critical Insights

### OBEX Search
**NEVER**: Filter by category first  
**ALWAYS**: Search all 113 objects with expanded terms  
**WHY**: 34 "misc" objects contain drivers, sensors, displays  

### Debug Visualization  
**FORMAT**: 8-bit indexed BMP, 256 colors  
**LAYERS**: Create multiple states (empty/full, on/off)  
**TOOLS**: Python with Pillow preferred  

### Hardware Testing
**COMPILE**: `pnut_ts -d program.spin2` (always use -d for debug)  
**DOWNLOAD**: `pnut-term-ts -r program.bin -p [device]`  
**MONITOR**: `tail -f logs/debug_*.log` (cleaner than console)  

### AI Navigation
**START**: `manifests/p2-knowledge-root.yaml`  
**FOLLOW**: Manifest tree (never guess paths)  
**REMEMBER**: P2 hardware ≠ complete peripherals (need OBEX)  

## 📋 Recommended Approaches

### OBEX Search Pattern
```yaml
1. Expand keywords: i2c → [i2c, iic, twi, two-wire, 2-wire]
2. Search all objects in all categories
3. Check top authors (jonnymac = 44 objects)
4. Return as: Highly Relevant, Related, Consider Also
```

### BMP Generation Pattern
```python
1. Parse description (dimensions, colors, elements)
2. Create 256-color palette
3. Generate layers (empty state, full state, overlays)
4. Provide Plot commands for cropping/display
```

### Testing Workflow
```bash
1. Compile: pnut_ts -d program.spin2
2. List devices: pnut-term-ts -n  
3. Download: pnut-term-ts -r program.bin -p P9cektn7 &
4. Monitor: tail -f logs/debug_$(date +%y%m%d)-*.log
```

## 🚨 Common Mistakes to Avoid

1. **Searching only "drivers" category** → Miss 64+ relevant objects
2. **Using console output** → Use log monitoring instead
3. **Forgetting -d flag** → No debug output without it
4. **Guessing file paths** → Always use manifest navigation
5. **Assuming P2 has UART/SPI/I2C** → These are OBEX objects!

## 💡 Pro Tips

- **Jon McPhalen's objects** (44 total) are production-quality
- **"misc" category** has 34 objects, many are drivers
- **Keyword expansion** dramatically improves discovery
- **Background execution** keeps console clean during testing
- **Layer BMPs** enable efficient state visualization