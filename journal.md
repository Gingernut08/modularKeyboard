# Devlog 1 — Initial Layout ([1.1](https://lapse.hackclub.com/timelapse/5RdF5y88RQ2I), [1.2](https://lapse.hackclub.com/timelapse/ZesBQOfE4MBa)) – Oliver

I started the project by creating the initial layout for the keyboard. I arranged the keys into their intended positions and added labels to identify each key. I also divided the keyboard into several sections, which will eventually become separate, detachable modules. This gave me a foundation to work from when designing the individual PCBs and the physical case.

# Devlog 2 — Case Top Plate ([2.1](https://lapse.hackclub.com/timelapse/eL3xCuvjLT37), [2.2](https://lapse.hackclub.com/timelapse/BLe_rd5PpnxV), [2.3](https://lapse.hackclub.com/timelapse/aRtAsJun4Mp-), [2.4](https://lapse.hackclub.com/timelapse/QBHegsUPQNaj)) – Oliver

I designed the top plate of the keyboard case, making sure that the switch positions matched the layout created previously. I used the standard 19.05 mm spacing between 1U keys to ensure compatibility with standard keyboard keycaps and layouts.

I added 14 × 14 mm square cut-outs for the switches, along with recessed wells around the keys to provide enough clearance for the keycaps to travel through their full range of motion without hitting the case. This is an important part of making sure the keyboard is comfortable and functional to use.

# Devlog 3 — Pogo Pin Connector Design ([3.1](https://lapse.hackclub.com/timelapse/cRwvfFemOQyj)) – Oliver

I designed a custom schematic symbol and PCB footprint for the connectors that will allow the different keyboard modules to communicate and share power.

The plan is to use magnetic pogo pin connectors, which will allow the modules to be attached and detached without needing traditional plug-and-socket connectors. I designed the footprint around the selected connectors, with the intention of connecting each PCB pad to its corresponding pogo pin using short wires.

This approach should make the keyboard more modular while keeping the connections compact and relatively easy to assemble.

Connector: [Magnetic Pogo Pin Connectors](https://www.amazon.co.uk/1Pair-Magnetic-Pogo-Pin-Connector-Black/dp/B0D1KRT3JL)

# Devlog 4 — Keycap Design ([4.1](https://lapse.hackclub.com/timelapse/chCaECsFfF9g0), [4.2](https://lapse.hackclub.com/timelapse/_NjUM8mT0LGT)) – Oliver

I created the 3D models for the keyboard's keycaps and positioned them according to the original layout. I included the different keycap sizes needed to accommodate the various rows, modifiers and larger keys.

The complete layout consists of:

- 97 × 1U keys
- 8 × 1.25U keys
- 2 × 1.5U keys
- 2 × 1.75U keys
- 4 × 2U keys
- 2 × 3U keys

Creating the keycaps in CAD allowed me to check the overall appearance and spacing of the keyboard before moving further into the physical design. It also helped ensure that the keycaps would fit within the wells designed into the top plate.

# Devlog 5 — Main Section PCB Routing ([5.1](https://lapse.hackclub.com/timelapse/dGQNtbVD7vZd), [5.2](https://lapse.hackclub.com/timelapse/8pVt1Rht81yD)) – Oliver

I started routing the main keyboard PCB, which contains the main alphanumeric section of the keyboard. This board includes the microcontroller, which will handle the keyboard's processing and communication, as well as the key matrix for detecting individual key presses.

I routed the connections for all 63 keys in this section, making sure that the matrix was connected correctly to the MCU. This is one of the largest sections of the keyboard and forms the foundation of the electronics.

# Devlog 6 — Battery Management, Function Row and Macro Keys ([6.1](https://lapse.hackclub.com/timelapse/crsrca5HazF8y), [6.2](https://lapse.hackclub.com/timelapse/_uE7_6aOiJ-wT)) – Oliver

Next, I worked on the battery management circuitry for the keyboard's LiPo battery. This circuitry will manage the battery's charging and power delivery, allowing the keyboard to operate wirelessly.

I also routed the key matrix for the function row and the additional macro keys. These keys will provide access to secondary functions and custom shortcuts, adding more functionality beyond the standard alphanumeric layout.

This stage brought together several important parts of the electronics, including the battery circuitry and additional key inputs.

# Devlog 7 — Final PCB Routing ([7.1](https://lapse.hackclub.com/timelapse/CuVCEyVKinYO)) – Oliver

I finished routing the remaining sections of the PCB, including the navigation cluster and the numpad. These sections complete the keyboard's full key layout and connect the remaining inputs to the electronics.

With the numpad and navigation sections routed, all of the keyboard's PCB sections are now complete.