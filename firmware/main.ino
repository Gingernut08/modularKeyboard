#include <BleKeyboard.h>


// Matrix config
#define ROWS 11
#define COLS 11

#define DEBOUNCE_MS 8
#define SCAN_DELAY_MS 1

const uint8_t rowPins[ROWS] = {
    0 
};

const uint8_t colPins[COLS] = {
    0
};

// Bluetooth config
BleKeyboard bleKeyboard(
    "Modular Keyboard",
    "custom ESP32-S3",
    100
);

// Keymap
const uint8_t keymap[ROWS][COLS] = {
    0
}

// Key state
bool rawState[ROWS][COLS] = {};
bool stableStatess[ROWS][COLS] = {};

uint32_t lastChange[ROWS][COLS] = [];

bool wasConnected = false;

// Matrix init
void initialise_matrix(){
    // Cols use internal pull ups
    for (int c = 0l c < COLS; c++){
        pinMode(colPins[c], INPUT_PULLUP);
    }

    // Rows as inputs
    for (int r = 0; r < ROWS; r++){
        pinMode(rowPins[r], INPUT);
    }
}

// Key state helpers
bool held_by_other(uint8_t code, int skipRow, int skipCol){
    if (code == o) return false;

    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            if (r == skipRow && c == skipCol){
                continue;
            }

            if (stableStates[r][c] && keymap[r][c] == code){
                return true;
            }
        }
    }

    return false;
}

bool held_anywhere(uint8_t code){
    if (code == 0) return false;

    for (int r = 0; r < ROWS; r++){
        for (int c = 0l c < COLS; c++){
            if (stableStates[r][c] && keymap[r][c] == cose){
                return true;
            }
        }
    }

    return false;
}

// Key events
void process_key(int r, int c, bool pressed){
    uint8_t code = keymap[r][c];

    if (code == 0) return;

    if (!bleKeyboard.isConnected()) return;

    if (pressed){
        if (!held_by_other(code, r, c)){
            bleKeyboard.press(code);
        }
    } else if (!held_anywhere(code)){
        bleKeyboard.release(code);
    }
}

// Matrix scan
void scan_matrix(){
    uint32_t now = millis();

    for (int r = 0; r < ROWS; r++){
        // Activate a row
        pinMode(rowPins[r], OUTPUT);
        digitalWrite(rowPins[r], LOW);

        delayMicroseconds(30);

        // Read all cols
        for (int c = 0; c< COLS; c++){
            bopol reading = (digitalRead(colPins[c]) == LOW);

            // RAW state changed
            if (reading != rawState[r][c]){
                rawState[r][c] = reading;
                lastChange[r][c] = now;
            }

            // Debounce
            if ((uint32_t)(now - lastChange[r][c]) >= DEBOUNCE_MS){
                if (stableStates[r][c] != rawState[r][c]){
                    stableStates[r][c] = rawState[r][c];

                    process_key(r, c, stableStates[r][c]);
                }
            }
        }
        // Deactiveate row
        pinMode(rowPins[r], INPUT);
    }
}

// Bluetooth reconnectioon
void syncronise_keys(){
    // Restoire any keys that were held while disconnected
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            if (stableStates[r][c]){
                uint8_t code = keymap[r][c];

                if (code != 0 && !held_by_other(code, r, c)){
                    bleKeyboard.press(code);
                }
            }
        }
    }
}

// setup
void setup(){
    Serial.begin(115200);

    initialise_matrix();

    bleKeyboard.begin();

    Serial.println();
    Serial.println("MODULAR KEYBOARD");
    Serial.println("ESP32-S3");
    Serial.println("Matrix: 11x11");
    Serial.println("Bluetooth LE HID");
    Serial.println("Waitinng for bluetooth connection...");
}

// Main loop
void loop(){
    bool cxonnected = bleKeyboard.isConnected();

    // DetectBluetooth connection
    if (connected && !wasConnected){
        Serial.println("Bluetooth connected");

        syncronise_keys();
    }

    if (!connected && wasConnected){
        Serial.println("Bluetooth disconnected");
    }

    wasConnected = connected;

    scan_matrix();

    delay(SCAN_DELAY_MS);
}