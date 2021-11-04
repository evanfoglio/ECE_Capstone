
def updateEngineCoolantTemp():
        img = ImageTk.PhotoImage( Image.open("Engine_coolant_temperature.png"))
        labelEngineCoolantTemp = ttk.Label(tabFFD1, image = img,  text= "Test")
        labelEngineCoolantTemp.image = img
        labelEngineCoolantTemp.grid(column=0, row=1)

def updateFuelPressure():
        img = ImageTk.PhotoImage( Image.open("Fuel_pressure.png"))
        labelFuelPressure = ttk.Label(tabFFD2, image = img,  text= "Test")
        labelFuelPressure.image = img
        labelFuelPressure.grid(column=0, row=1)

def updateEngineSpeed():
        img = ImageTk.PhotoImage( Image.open("Engine_speed.png"))
        labelEngSpeed = ttk.Label(tabFFD3, image = img,  text= "Test")
        labelEngSpeed.image = img
        labelEngSpeed.grid(column=0, row=1)

def updateVehicleSpeed():
        img = ImageTk.PhotoImage( Image.open("Vehicle_speed.png"))
        labelVehicleSpeed = ttk.Label(tabFFD4, image = img,  text= "Test")
        labelVehicleSpeed.image = img
        labelVehicleSpeed.grid(column=0, row=1)

def updateIntakeAirTemperature():
        img = ImageTk.PhotoImage( Image.open("Intake_air_temperature.png"))
        labelIntakeAirTemperature = ttk.Label(tabFFD5, image = img,  text= "Test")
        labelIntakeAirTemperature.image = img
        labelIntakeAirTemperature.grid(column=0, row=1)

def updateThrottlePosition():
        img = ImageTk.PhotoImage( Image.open("Throttle_position.png"))
        labelThrottlePosition = ttk.Label(tabFFD6, image = img,  text= "Test")
        labelThrottlePosition.image = img
        labelThrottlePosition.grid(column=0, row=1)

def updateFuelTankLevelInput():
        img = ImageTk.PhotoImage( Image.open("Fuel_Tank_Level_Input.png"))
        labelFuelTankLevelInput = ttk.Label(tabFFD7, image = img,  text= "Test")
        labelFuelTankLevelInput.image = img
        labelFuelTankLevelInput.grid(column=0, row=1)

def updateFuelType():
        img = ImageTk.PhotoImage( Image.open("Fuel_Type.png"))
        labelFuelType = ttk.Label(tabFFD8, image = img,  text= "Test")
        labelFuelType.image = img
        labelFuelType.grid(column=0, row=1)

def updateEngineOilTemperature():
        img = ImageTk.PhotoImage( Image.open("Engine_oil_temperature.png"))
        labelEngineOilTemperature = ttk.Label(tabFFD9, image = img,  text= "Test")
        labelEngineOilTemperature.image = img
        labelEngineOilTemperature.grid(column=0, row=1)

