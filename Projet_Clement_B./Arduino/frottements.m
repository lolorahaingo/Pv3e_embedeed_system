%% Arduino with hall effect boys
close all
clearvars
clc

s = serial('COM10');
set(s,'BaudRate',115200);
fopen(s);

fprintf(s,'*IDN?');
out = fscanf(s);

fclose(s);
delete(s);
clear s;