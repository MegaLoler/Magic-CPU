# Runic

This is a C-like language for higher level magic programming!

## How to build

To build the Runic compiler, do this:
```bash
make
```

The compiler binary will be located in `build/runic.bin`

## How to use

To use the Runic compiler to compile a Runic program, do this:

```bash
python ../assembler.py build/runic.bin your_program.spell
```

To run the test spell, you can simply do this:
```bash
make test
```
