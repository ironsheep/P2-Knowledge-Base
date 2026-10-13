# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in an example's header (the manual, the version, where it appears, the dates)
is read from the repository at sync time. This is the sentence a person writes.

Keep it to one line, and say what the example *shows*, not what it *is*.

- `ch02-text-inline.spin2`: Two statements carrying their descriptive text inline, so every character of it is DEBUG data
- `ch02-text-in-dat.spin2`: The same two messages with their text moved into DAT and printed with zstr_(), so the statements become one record
- `ch02-line-buffer.spin2`: A whole line built in a hub buffer from DAT labels and digits, then printed by one debug() statement
- `ch02-share-records.spin2`: Identical statements sharing one record, and labelled statements that look alike becoming separate records
- `ch02-channels.spin2`: One channel per subsystem under DEBUG_MASK, with the masked-off channel compiled out of the build
- `ch02-sensor-driver.spin2`: A child object whose channelled output is silent unless the parent turns its channel on
- `ch02-light-a-child.spin2`: A parent turning on a child's debug channel where it declares the object
