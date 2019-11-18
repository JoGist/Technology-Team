def decideTurn(self): # TODO: resolve those nested conditions
    speed1 = 120
    speed2 = 160
    th = self.theta; dt = self.degree_target; case = 0;
    if dt >= 0 and th >= dt - 180 and th < dt:
        c = 1
    elif dt >= 0 and th < dt - 180 and th > dt:
        c = 2
    elif dt < 0 and th <= dt + 180 and th > dt:
        c = 3
    else:
        c = 4

    switch (c) {
        case 1: self.motors.setTurnRight()
                if self.theta >= self.degree_target - 30:
                    self.speed = speed1
                else:
                    self.speed = speed2
                break

        case 2: self.motors.setTurnLeft()
                if self.degree_target < 150 and self.theta <= self.degree_target + 30 and self.theta > self.degree_target:
                    self.speed = speed1
                elif self.degree_target > 150 and self.theta <= self.degree_target - 330:
                    self.speed = speed1
                elif self.degree_target > 150 and self.theta >= self.degree_target:
                    self.speed = speed1
                else:
                    self.speed = speed2
                break

        case 3: self.motors.setTurnLeft()
                if self.theta <= self.degree_target + 30:
                    self.speed = speed1
                else:
                    self.speed = speed2
                break

        case 4: self.motors.setTurnRight()
                if self.degree_target > -150 and self.theta >= self.degree_target - 30 and self.theta < self.degree_target:
                    self.speed = speed1
                elif self.degree_target < -150 and self.theta >= self.degree_target + 330:
                    self.speed = speed1
                elif self.degree_target < -150 and self.theta <= self.degree_target:
                    self.speed = speed1
                else:
                    self.speed = speed2
                break
    }

    print(str(self.degree_target)+", "+str(self.theta)+", "+str(self.speed))
