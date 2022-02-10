function pinHandler(arduino, valve, time)

    if valve == 1
        pin_no = 8;
    elseif valve == 2
        pin_no = 9;
    elseif valve == 3
        pin_no = 10;
    elseif valve == 4
        pin_no = 11;
    elseif valve == 5
        pin_no = 12;
    elseif valve == 6
        pin_no = 7;
    end

    if pin_no>=10
        serial_code_on = "1"+num2str(pin_no);
        serial_code_off = "0"+num2str(pin_no);
    else
        serial_code_on = "1"+num2str(0)+num2str(pin_no);
        serial_code_off = "0"+num2str(0)+num2str(pin_no);
    end

    write(arduino, serial_code_on, "string")
    pause(time)
    write(arduino, serial_code_off, "string")