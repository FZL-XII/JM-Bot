import pikepdf


def encrypt(src, dst, password):
    with pikepdf.open(src) as pdf:
        pdf.save(
            dst,
            encryption=pikepdf.Encryption(
                user=password,
                owner=password,
                R=4,
            )
        )
