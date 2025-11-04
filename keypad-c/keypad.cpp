/* ECEGRE-2020 - Seattle University
   Description: Homework#4 Keypad class file
   Authors: 
*/

#include <string>
#include <wiringPi.h>
#include "keypad.h"

using namespace std;

Keypad::Keypad(int columnInPins[MAXCOL], int rowInPins[MAXROW]){
    //Setup wiringPi
    wiringPiSetupGpio();
    
    //Check for duplicate pin numbers
    for (int i = 0; i < MAXCOL; i++) {
        for (int j = 0; j < MAXCOL; j++) {
            if (i != j && columnInPins[i] == columnInPins[j]) throw "Invalid Custom Pinout: There are Duplicate Pins";
        }
        for (int j = 0; j < MAXROW; j++) {
            if (columnInPins[i] == rowInPins[j]) throw "Invalid Custom Pinout: There are Duplicate Pins";
        }
    }
    
    for (int i = 0; i < MAXROW; i++) {
        for (int j = 0; j < MAXROW; j++) {
            if (i != j && rowInPins[i] == rowInPins[j]) throw "Invalid Custom Pinout: There are Duplicate Pins";
        }
    }
    
    //Check for invalid Pin numbers or length of array and set the custom pinouts if they are valid
    for (int i = 0; i < MAXCOL; i++) {
        if (columnInPins[i] <= 27) column[i] = columnInPins[i];
        else throw "Invalid Custo Column Pinout";
    }

    for (int i = 0; i < MAXROW; i++) {
        if (rowInPins[i] <= 27) row[i] = rowInPins[i];
        else throw "Invalid Custom Row Pinout";
    }

    //Initialize booleans
    digit_ready = false;
    is_stopped = true;
}

void Keypad::run(){
    //If the get key thread is stopped start the thread
    if (is_stopped) {
        //Try catch in case we can't start the thread
        try {
            get_key_thread = new jthread(&Keypad::get_key, this);
            is_stopped = false;
        } catch(...) {
            cerr << "Couldn't start thread";
        }
    }
}

void Keypad::get_key() {
    //Run while true in order to run forever while the thread isn't stopped
    while(true) {
        //If the thread is stopped exit the while loop
        if (is_stopped) break;
        
        //Short delay at the start of each run of the thread
        this_thread::sleep_for(10ms);
        
        //Set the column pins to output low
        for (int i = 0; i < MAXCOL; i++) {
            pinMode(this->column[i], OUTPUT);
            digitalWrite(this->column[i], 0);
        }
        
        //Set the row pins to input with pull up resistor
        for (int i = 0; i < MAXROW; i++) {
            pinMode(this->row[i], INPUT);
            pullUpDnControl(this->row[i], PUD_UP);
        }
        
        //Check for if a key is pressed and set row_val to the row number of the pressed key
        int row_val = -1;
        for (int i = 0; i < MAXROW; i++) {
            if (digitalRead(this->row[i]) == 0) row_val = i;
        }
        
        //If a key wasn't pressed restart the loop
        if (row_val < 0 || row_val >= MAXROW) {
            this->last_digit = "";
            this->digit_ready = false;
            continue;
        }
        
        //Set the columns to input with pull down resistor
        for (int i = 0; i < MAXCOL; i++) {
            pinMode(this->column[i], INPUT);
            pullUpDnControl(this->column[i], PUD_DOWN);
        }
        
        //Set the pressed row to output high
        pinMode(this->row[row_val], OUTPUT);
        digitalWrite(this->row[row_val], 1);
        
        //Set col_val to the column number of the key pressed
        int col_val = -1;
        for(int i = 0; i < MAXCOL; i++) {
            if (digitalRead(this->column[i]) == 1) col_val = i;
        }

        //If it's an invalid column number restart the loop
        if (col_val < 0 || col_val >= MAXCOL) {
            this->last_digit = "";
            this->digit_ready = false;
            continue;
        }
        
        //Tell the class that the digit is ready and set the right digit to last_digit
        if (!this->digit_ready) {
            this->digit_ready = true;
            this->last_digit = KEYPAD[row_val][col_val];
        }
    }
}

string Keypad::get_digit(){
    //Take user input based on get_key above and prepare for new digit
    while(true){
        if (this->digit_ready){
            this->digit_ready = false;
            string temp = last_digit;
            last_digit = "";
            return temp;
        }
        this_thread::sleep_for(0.1s);
    }
}

//End the thread
void Keypad::stop() {
    is_stopped = true;
    get_key_thread->join();
}