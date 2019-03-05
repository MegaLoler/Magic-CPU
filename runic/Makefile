SRC_DIR=src
BUILD_DIR=build
TEST_DIR=test

TARGET=runic
ASSEMBLER=../assembler.py
INTERPRETER=../run.py

TARGET_BIN=$(BUILD_DIR)/$(TARGET).rune
TARGET_SRC=$(SRC_DIR)/$(TARGET).asm
TARGET_TEST=$(TEST_DIR)/$(TARGET).spell

DEPS=$(SRC_DIR)/*

$(TARGET_BIN): $(DEPS)
	mkdir -p $(BUILD_DIR)
	$(ASSEMBLER) $(TARGET_SRC) $(TARGET_BIN)

.PHONY: clean

clean:
	mkdir -p $(BUILD_DIR)
	rm $(BUILD_DIR)/*

.PHONY: test

test: $(TARGET_BIN)
	$(INTERPRETER) $(TARGET_BIN) $(TARGET_TEST)

