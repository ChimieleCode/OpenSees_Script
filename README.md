# OpenSees_Script
a script to make presss and pres-lam modeling

HP:
-All the Seismic-Resistant frames are along the Y axis
-All the Seismic-Resistant frames are equal in span and sections
-Every span is the same
-Every storey is the same
-All the columns are the same
-All beams from a given floor share same sections
-Levels only describe storeys
-ONLY Seismic-Resistant MUST be included in the analytical model

THE USER HAVE TO:
-Specify Mass of the building
-The Heff of the equivalent SDOF
-M-theta of connections [7 strain-stress points for PT/N and Hardening params for S]
-The young module of the elements [Concrete or Timber or Else]
-Specify the params of the Push-Pull Analysis
