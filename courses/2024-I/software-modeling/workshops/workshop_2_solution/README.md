# Workshop 2 - Solution

This is a workshop related with a backend system to provide a vehicles catalog using python and patterns design.

## Requirements

The requirements for this workshop are presented as follows:
- Cars must have next attributes: transmission, chassis, year, trade, model, combustible
type, and engine.
- Yacht must have next attributes: length, weight, year, trade, model, engine.
- Trucks and Motorcycles will keep same attributes as before. However, just for trucks
you need to calculate the gas consumption due to regulations of both USA and Europe.
- You need to add next vehicles options, and you must define the appropriate atteibutes
they need: Helicopter, Scooter.
- Create engines in the platform is not a good idea due to possible human errors. So,
it is a better idea to have some predefined engines per each one of the vehicles types,
divider in gas and electric engines. Also, per each vehicle you should define low gama
and high gama engine.
All engines must have next attributes: stability, power, weight, dimensions, torque,
and maximum speed.
- You must reduce memory as much as possible, so check where you could reduce the
creation of duplicates objects to avoid. Be careful with memory references.
You must deliver a technical report where a Class Diagram of your solution is pro-
vided; here it is recommended to think in components, deﬁne a diagram por each component
where connections with other components will be absolutely clear. Also, you must write
about technical concerns and decisions you make to create the architecture you are propos-
ing .
- Something had been missed: every vehicle must have a price, and in the searches
the users would like to search by price range.


## Business Rules

- Every vehicle just have chassis of type A or B.
- Gas consumption is based on engine information...
- Gas consumption is based on next equation. 
  `1.1 ∗ engine.potency + 0.2 ∗ engine.weight - (0.3 if A or 0.5 if B)`
