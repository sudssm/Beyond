/* IR sensor */

local pin9 = hardware.pin9
pin9.configure(ANALOG_IN)

local irOn = false
local size = 10000

while(true) {
    local avg = 0
    for (local j = 0; j < size; j++) {
        avg += pin9.read()
    }
    avg = 1.0 * avg / size
    
    if (avg < 65000) {
        if (!irOn) {
            agent.send("update", "update");
        }
        irOn = true
    } else {
        irOn = false
    }
}
