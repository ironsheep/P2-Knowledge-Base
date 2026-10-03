::: caution
**Who meets it:** the same programs as Erratum E4: a `GETXACC` reading taken after each DDS/Goertzel burst.

**What you see:** each reading lacks the burst's last term. That term is added on the first clock of the next Goertzel burst.

**What to do:** run a short burst whose terms are all zero before you read. The `burst_sums` routine, shared with Erratum E4, does this in SINC1 mode.
:::
