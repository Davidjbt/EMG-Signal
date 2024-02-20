#include <EMGFilters.h>

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include "EMGFilters.h"
#include <Servo.h>

#define TIMING_DEBUG 1

#define SensorInputPin A0

EMGFilters myFilter;
int sampleRate = SAMPLE_FREQ_1000HZ;
int humFreq = NOTCH_FREQ_50HZ;

static int Threshold = 10;

unsigned long timeStamp;
unsigned long timeBudget;

Servo myServo;
const int numSamples = 150; // Adjust the number of samples for rolling average
int window[numSamples];
int sampleIndex = 0;
int state = 0;

void setup() {
    myFilter.init(sampleRate, humFreq, true, true, true);

    Serial.begin(115200);

    timeBudget = 1e6 / sampleRate;

    myServo.attach(A1);
    for (int i = 0; i < numSamples; ++i) {
      window[i] = 0;
    }
}

void loop() {
    timeStamp = micros();

    int Value = analogRead(SensorInputPin);
    int DataAfterFilter = myFilter.update(Value);

    int envlope = abs(DataAfterFilter);

    timeStamp = micros() - timeStamp;
    // Serial.println(envlope);

    // Update the rolling average
    window[sampleIndex] = envlope;
    sampleIndex = (sampleIndex + 1) % numSamples;
    int sum = 0;
    for (int i = 0; i < numSamples; ++i) {
        sum += window[i];
    }
    int rollingAverage = sum / numSamples;

    Serial.println(rollingAverage);

    if (rollingAverage > Threshold) {
      myServo.write(180);
    } else {
      myServo.write(0);
    }

    delayMicroseconds(500);
}