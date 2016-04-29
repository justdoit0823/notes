
def _save(im, fp, filename):

    try:
        rawmode = RAWMODE[im.mode]
    except KeyError:
        raise IOError("cannot write mode %s as JPEG" % im.mode)

    # Image.save时指定的参数
    info = im.encoderinfo

    # 指定dpi信息
    dpi = info.get("dpi", (0, 0))

    quality = info.get("quality", 0)
    subsampling = info.get("subsampling", -1)
    qtables = info.get("qtables")

    if quality == "keep":
        quality = 0
        subsampling = "keep"
        qtables = "keep"
    elif quality in presets:
        preset = presets[quality]
        quality = 0
        subsampling = preset.get('subsampling', -1)
        qtables = preset.get('quantization')
    elif not isinstance(quality, int):
        raise ValueError("Invalid quality setting")
    else:
        if subsampling in presets:
            subsampling = presets[subsampling].get('subsampling', -1)
        if isStringType(qtables) and qtables in presets:
            qtables = presets[qtables].get('quantization')

    if subsampling == "4:4:4":
        subsampling = 0
    elif subsampling == "4:2:2":
        subsampling = 1
    elif subsampling == "4:1:1":
        subsampling = 2
    elif subsampling == "keep":
        if im.format != "JPEG":
            raise ValueError(
                "Cannot use 'keep' when original image is not a JPEG")
        subsampling = get_sampling(im)

    def validate_qtables(qtables):
        if qtables is None:
            return qtables
        if isStringType(qtables):
            try:
                lines = [int(num) for line in qtables.splitlines()
                         for num in line.split('#', 1)[0].split()]
            except ValueError:
                raise ValueError("Invalid quantization table")
            else:
                qtables = [lines[s:s+64] for s in range(0, len(lines), 64)]
        if isinstance(qtables, (tuple, list, dict)):
            if isinstance(qtables, dict):
                qtables = convert_dict_qtables(qtables)
            elif isinstance(qtables, tuple):
                qtables = list(qtables)
            if not (0 < len(qtables) < 5):
                raise ValueError("None or too many quantization tables")
            for idx, table in enumerate(qtables):
                try:
                    if len(table) != 64:
                        raise
                    table = array.array('b', table)
                except TypeError:
                    raise ValueError("Invalid quantization table")
                else:
                    qtables[idx] = list(table)
            return qtables

    if qtables == "keep":
        if im.format != "JPEG":
            raise ValueError(
                "Cannot use 'keep' when original image is not a JPEG")
        qtables = getattr(im, "quantization", None)
    qtables = validate_qtables(qtables)

    extra = b""

    icc_profile = info.get("icc_profile")
    if icc_profile:
        ICC_OVERHEAD_LEN = 14
        MAX_BYTES_IN_MARKER = 65533
        MAX_DATA_BYTES_IN_MARKER = MAX_BYTES_IN_MARKER - ICC_OVERHEAD_LEN
        markers = []
        while icc_profile:
            markers.append(icc_profile[:MAX_DATA_BYTES_IN_MARKER])
            icc_profile = icc_profile[MAX_DATA_BYTES_IN_MARKER:]
        i = 1
        for marker in markers:
            size = struct.pack(">H", 2 + ICC_OVERHEAD_LEN + len(marker))
            extra += (b"\xFF\xE2" + size + b"ICC_PROFILE\0" + o8(i) +
                      o8(len(markers)) + marker)
            i += 1

    # get keyword arguments
    im.encoderconfig = (
        quality,
        # "progressive" is the official name, but older documentation
        # says "progression"
        # FIXME: issue a warning if the wrong form is used (post-1.1.7)
        "progressive" in info or "progression" in info,
        info.get("smooth", 0),
        "optimize" in info,
        info.get("streamtype", 0),
        dpi[0], dpi[1],
        subsampling,
        qtables,
        extra,
        info.get("exif", b"")
        )

    # if we optimize, libjpeg needs a buffer big enough to hold the whole image
    # in a shot. Guessing on the size, at im.size bytes. (raw pizel size is
    # channels*size, this is a value that's been used in a django patch.
    # https://github.com/matthewwithanm/django-imagekit/issues/50
    bufsize = 0
    if "optimize" in info or "progressive" in info or "progression" in info:
        # keep sets quality to 0, but the actual value may be high.
        if quality >= 95 or quality == 0:
            bufsize = 2 * im.size[0] * im.size[1]
        else:
            bufsize = im.size[0] * im.size[1]

    # The exif info needs to be written as one block, + APP1, + one spare byte.
    # Ensure that our buffer is big enough
    bufsize = max(ImageFile.MAXBLOCK, bufsize, len(info.get("exif", b"")) + 5)

    ImageFile._save(im, fp, [("jpeg", (0, 0)+im.size, 0, rawmode)], bufsize)
