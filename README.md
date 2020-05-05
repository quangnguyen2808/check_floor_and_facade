# COUNT FLOOR AND FACADE (VER 1)

This code will extract the number of floor and facade from a description.

Only use basic algorithm.

## Getting Started

### Prerequisites

* Python 3.6+

* pandas

* underthesea

* regex

## Installation

### Clone

Clone this repo to your local machine using git clone https://github.com/quangnguyen2808/check_floor_and_facade.git

### Test

- Count facade in a description/text.

  - if 'kiệt' exists -> 0
  
  - if only 'mặt tiền' exists -> 1
  
  - if 'mặt tiền' exists with a number n before that -> n
  
  - if no mention -> default = 1

```
#   Count facade
def check_facade(text):
    # Default facade = 1
    facade = 1
    if 'kiệt' in text:
        facade = 0
    elif 'mặt tiền' in text:
        pos = text.find('mặt tiền')
        try:
            # case 'n mặt tiền'
            facade = float(text[pos-2])
        except:
            facade = 1
    return facade
```

- Count floor in a description/text.
  
  Find position of 'tầng'
  
  - if position = -1 -> no mention -> default floor = 1
  
  - if position != -1: Check 3 cases:
    
      - '3.5 tầng'
      - '. 2 tầng'
      - '2 tầng'
  
  - Problem with case: '... nhà cấp 4.2 tầng ...'
  
```
def check_floor(text):
    floor = 1
    pos = text.find('tầng')
    if pos != -1:
        # case '3.5 tầng'
        sequence = text[pos-4:pos].replace(',', '').replace(',', '').strip()
        try:   
            floor = float(sequence)/10 if float(sequence) > 10 else float(sequence)
        except:
            try:
                # case '3 tầng'
                floor = float(sequence[-1])
            except:
                pass
    return floor
```
