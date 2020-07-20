# Conclusions on the choice of sensor
1. All the sensors are fine to measure distance.
2. Only servodrive is able to measure acceleration correctly.
3. Encoder does not bring any advantage to the experiment.
4. Force data will be synchronized
based on the distance measured with potentiometer
by minimizing mean squared error.
5. Resampling can be done by a pandas built-in rolling method instead of custom function.
