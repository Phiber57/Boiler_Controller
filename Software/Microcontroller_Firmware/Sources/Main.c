/** @file Main.c
 * Boiler controller entry point and main loop.
 * @author Adrien RICCIARDI
 */
#include <ADC.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <Led.h>
#include <Mixing_Valve.h>
#include <Protocol.h>
#include <Relay.h>
#include <Temperature.h>
#include <util/delay.h>

//-------------------------------------------------------------------------------------------------
// Private variables
//-------------------------------------------------------------------------------------------------
/** Configure microcontroller fuses. */
FUSES =
{
	FUSE_CKSEL3, // Fuses low byte : use the longest power-on delay to make sure power supply voltage is stabilized when core starts, select a full swing crystal oscillator with brown-out detection enabled
	FUSE_SPIEN & FUSE_EESAVE, // Fuses high byte : enable Serial programming and Data Downloading, keep EEPROM content when erasing the chip, give less room possible to the bootloader (for now)
	FUSE_BODLEVEL2 // Fuses extended byte : set brown-out reset voltage to approximately 4.3V
};

/** External sensor temperature (in °C). */
static signed char Main_Temperature_Outside = 0;
/** The pipe going to the radiators' temperature. */
static signed char Main_Temperature_Radiator_Start = 0;
/** The pipe coming from the radiators' temperature. */
static signed char Main_Temperature_Radiator_Return = 0;

//-------------------------------------------------------------------------------------------------
// Entry point
//-------------------------------------------------------------------------------------------------
int main(void) // Can't use void return type because it triggers a warning
{
	unsigned char Is_WiFi_Successfully_Initialized, Is_Status_Led_On = 1;
	
	// Initialize modules
	LedInitialize();
	LedTurnOn(LED_ID_STATUS); // Turn status led on to tell controller is booting
	ADCInitialize();
	RelayInitialize();
	MixingValveInitialize();
	Is_WiFi_Successfully_Initialized = ProtocolInitialize();
	
	// Enable interrupts now that all modules have been configured
	sei();
	
	// Tell whether network is working
	if (!Is_WiFi_Successfully_Initialized) LedTurnOn(LED_ID_NETWORK_ERROR);
	
	// Start pump
	RelayTurnOn(RELAY_ID_PUMP);
	
	while (1)
	{
		// Sample all analog values
		ADCTask();
		
		// Cache converted temperature values (conversion computations are cost a lot of cycles)
		Main_Temperature_Outside = TemperatureGetCelsiusValue(TEMPERATURE_ID_OUTSIDE);
		Main_Temperature_Radiator_Start = TemperatureGetCelsiusValue(TEMPERATURE_ID_RADIATOR_START);
		Main_Temperature_Radiator_Return = TemperatureGetCelsiusValue(TEMPERATURE_ID_RADIATOR_RETURN);
		
		// Make the mixing valve moves
		MixingValveTask();
		
		// Tell that controller is still alive
		if (Is_Status_Led_On)
		{
			LedTurnOn(LED_ID_STATUS);
			Is_Status_Led_On = 0;
		}
		else
		{
			LedTurnOff(LED_ID_STATUS);
			Is_Status_Led_On = 1;
		}
		
		// This is a slow regulation process, we can safely wait some time between each loop
		_delay_ms(1000);
	}
}
