# PhotoshopAPI Enumerations

All accessed via `psapi.enum.<EnumName>.<value>`.

## ColorMode
`rgb`, `cmyk`, `grayscale`

## BitDepth
`bd_8` (uint8), `bd_16` (uint16), `bd_32` (float32)

## ChannelID
`red`, `green`, `blue`, `cyan`, `magenta`, `yellow`, `black`, `gray`, `custom`, `mask`, `alpha`

## Compression
- `raw` — no compression
- `rle` — run-length encoding, fastest writes
- `zip` — deflate
- `zipprediction` — zip + delta prediction (default, best for most cases)

## BlendMode
`passthrough` (groups only), `normal`, `dissolve`, `darken`, `multiply`, `colorburn`, `linearburn`, `darkercolor`, `lighten`, `screen`, `colordodge`, `lineardodge`, `lightercolor`, `overlay`, `softlight`, `hardlight`, `vividlight`, `linearlight`, `pinlight`, `hardmix`, `difference`, `exclusion`, `subtract`, `divide`, `hue`, `saturation`, `color`, `luminosity`

## LayerColor
`none`, `red`, `orange`, `yellow`, `green`, `blue`, `violet`, `gray`, `seafoam`, `indigo`, `magenta`, `fuschia`

## LinkedLayerType
`data` (embedded), `external` (linked file on disk)

## Text Enums

### WritingDirection
`horizontal`, `vertical`

### ShapeType
`point_text`, `box_text`

### WarpStyle
`no_warp`, `arc`, `arc_lower`, `arc_upper`, `arch`, `bulge`, `shell_lower`, `shell_upper`, `flag`, `wave`, `fish`, `rise`, `fish_eye`, `inflate`, `squeeze`, `twist`, `custom`

### FontType
`open_type`, `true_type`

### FontCaps
`normal`, `small_caps`, `all_caps`

### FontBaseline
`normal`, `superscript`, `subscript`

### Justification
`left`, `right`, `center`, `justify_last_left`, `justify_last_right`, `justify_last_center`, `justify_all`

### AntiAliasMethod
`no_anti_alias`, `crisp`, `strong`, `smooth`, `sharp`
