/* ECEGRE-2020 - Seattle University
   Description: Homework#4 main for running a keypad and printing output
   Authors: 
*/

#include <iostream>  // cout, cerr
#include <csignal>   // signal, SIGINT
#include <signal.h>  // usleep
#include "keypad.h"  // Keypad

using namespace std;

int main(){
    // Declare and initialize variables to be used
    
    // Output a helper message to the console output

    // Set up and begin keypad operation, checking for valid pinout
    
    // Start the keypad thread

    // try
        // Start infinite loop to
            // Get digit typed into keypad
            // If * is pressed, backspace
            // If # is pressed, go to a new line
            // Otherwise, print to the console the digit
            // Wait for 500ms
    // catch Ctrl+c

    // End the keypad's operation (stop keypad thread, delete the keypad object if using heap)
    
    return 0;
}