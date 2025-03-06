# NDCompression
Compression by recognising data patterns in multiple dimensions.

## Format
Total: 
- Shape: u15
- Direction: u16 # | Max = Dimensions * 2 |
- Length u7
- Type: u2 # | (Raw || Constant || Interval || Repeat) |
  - Raw: void,
  - Constant: u8
  - Interval: {u8, u8}
  - Repeat: !TODO!