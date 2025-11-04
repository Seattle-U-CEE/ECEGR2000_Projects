/* ECEGRE-2020 - Seattle University
   Description: Homework#4 Header file for keypad class
   Authors: 
*/

#include <string>
#include <iostream>  // cerr
#include <thread>    // jthread, this_thread::sleep_for, get_key_thread

#pragma once  // cause the current source file to be included only once in a single compilation

//Size of column and row for keypad
#define MAXCOL 3
#define MAXROW 4

using namespace std;

class Keypad
{
    private:
        bool digit_ready;
        bool is_stopped;
        jthread* get_key_thread;
        const string KEYPAD[MAXROW][MAXCOL] ={
            {"1","2","3"},
            {"4","5","6"},
            {"7","8","9"},
            {"*","0","#"}
        };
        int column[MAXCOL];
        int row[MAXROW];
        string last_digit;

    public:
            
        //Constructors
        Keypad(int columnInPins[MAXCOL], int rowInPins[MAXROW]);
        
        //Start the keypad
        void run(void);
        
        //Set values based on keypad pressed
        void get_key();
        
        //Return value of key
        string get_digit(void);
        
        //Stops thread
        void stop();
};