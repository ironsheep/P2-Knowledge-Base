# Example purposes — P2AN007

One line per shipped example. `sync-manual-examples.py` reads these into the
generated header's `Purpose....` field; it will not invent one. ASCII only —
the header is `.spin2` source, and the authoring guide's rule is absolute.

- `in-cog-record.spin2` — Group related fields such as a sensor reading's timestamp, value and status into one named STRUCT record in an array, instead of three parallel arrays
- `spsc-ring-buffer.spin2` — Stream records from exactly one producer cog to one consumer cog through a ring buffer, with no lock
- `latest-wins-mailbox.spin2` — Send commands from one cog to another where only the newest matters, published with a sequence counter and no lock
- `locked-multiwriter-queue.spin2` — Feed one queue from several cogs, with a P2 hardware lock making each enqueue exclusive
- `single-long-packed-record.spin2` — Pack a whole record into one long with member bitfields so it publishes in a single atomic store
- `packed-header-offsets.spin2` — Address a packed header through raw addresses while OFFSETOF supplies each member offset instead of hand-counted numbers
