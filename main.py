from datetime import datetime

# Constants for month and day lengths
MONTH_LENGTHS = {0: 31, 1: 29, 2: 31, 3: 30, 4: 31, 5: 30, 6: 31, 7: 31, 8: 30, 9: 31, 10: 30, 11: 31}
MONTHS = {0: "January", 1: "February", 2: "March", 3: "April", 4: "May", 5: "June", 6: "July", 7: "August", 8: "September", 9: "October", 10: "November", 11: "December"}

# Tzolkin and Haab month names
TZOLKIN_MONTHS = {i: name for i, name in enumerate(["Imix'", "Ik'", "Ak'b'al", "K'an", "Chikchan", "Kimi", "Manik'", "Lamat", "Muluk", "Ok", "Chuwen", "Eb'", "B'en", "Ix", "Men", "k'ib'", "kab'an", "Etz'nab'", "Kawak", "Ajaw"])}
HAAB_MONTHS = {i: name for i, name in enumerate(["Pop", "Wo'", "Sip", "Sotz'", "Sek", "Xul", "Yaxk'in", "Mol", "Ch'en", "Yax", "Sak'", "Keh", "Mak", "K'ank'in", "Muwan", "Pax", "K'ayab", "kumk'u", "Wayeb'"])}

def validate_date(m, d, y):
    if d > MONTH_LENGTHS[m]:
        print(f"{MONTHS[m]} does not contain {d} days.")
        return False
    if d < 1:
        print("Days must be a positive number")
        return False
    if y == 0:
        print("Julian calendar used by historians does not have a year zero.")
        return False
    if y > 4000 or y < -4000:
        print("Please enter a year between -4000 (B.C.) and 4000 (A.D.)")
        return False
    if m == 1 and d == 29:
        if y % 4 != 0 or (y > 1582 and y % 100 == 0 and y % 400 != 0):
            print(f"{MONTHS[m]} does not contain {d} days for the year {y}")
            return False
    return True

def to_jdn(m, d, y):
    if m <= 1:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4 if y > 1582 or (y == 1582 and (m > 10 or (m == 10 and d > 15))) else 0
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524

def to_long_count(jdn):
    # Using the standard correlation constant 584283
    long_count = round(jdn - 584283)
    baktun = long_count // 144000
    long_count %= 144000
    katun = long_count // 7200
    long_count %= 7200
    tun = long_count // 360
    long_count %= 360
    uinal = long_count // 20
    kin = long_count % 20
    return baktun, katun, tun, uinal, kin

def to_tzolkin(jdn):
    # Using the standard correlation constant 584283
    long_count = round(jdn - 584283)
    day_number = ((long_count + 3) % 13) + 1
    day_name = (long_count + 19) % 20
    return day_number, TZOLKIN_MONTHS[day_name]

def to_haab(jdn):
    # Using the standard correlation constant 584283
    long_count = round(jdn - 584283)
    day_of_haab = (long_count + 348) % 365
    day = day_of_haab % 20
    month = day_of_haab // 20
    return day, HAAB_MONTHS[month]

# Example usage
m, d, y = 8, 25, 2024  # March 25, 1990
if validate_date(m - 1, d, y):
    jdn = to_jdn(m, d, y)
    long_count = to_long_count(jdn)
    tzolkin = to_tzolkin(jdn)
    haab = to_haab(jdn)
    print(f"Long Count: {'.'.join(map(str, long_count))}")
    print(f"Tzolkin: {tzolkin[0]} {tzolkin[1]}")
    print(f"Haab: {haab[0]} {haab[1]}")
