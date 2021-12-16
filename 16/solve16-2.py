# Sem arquivo input16.txt desta vez
data_hex = '4057231006FF2D2E1AD8025275E4EB45A9ED518E5F1AB4363C60084953FB09E008725772E8ECAC312F0C18025400D34F732333DCC8FCEDF7CFE504802B4B00426E1A129B86846441840193007E3041483E4008541F8490D4C01A89B0DE17280472FE937C8E6ECD2F0D63B0379AC72FF8CBC9CC01F4CCBE49777098D4169DE4BF2869DE6DACC015F005C401989D0423F0002111723AC289DED3E64401004B084F074BBECE829803D3A0D3AD51BD001D586B2BEAFFE0F1CC80267F005E54D254C272950F00119264DA7E9A3E9FE6BB2C564F5376A49625534C01B0004222B41D8A80008446A8990880010A83518A12B01A48C0639A0178060059801C404F990128AE007801002803AB1801A0030A280184026AA8014C01C9B005CE0011AB00304800694BE2612E00A45C97CC3C7C4020A600433253F696A7E74B54DE46F395EC5E2009C9FF91689D6F3005AC0119AF4698E4E2713B2609C7E92F57D2CB1CE0600063925CFE736DE04625CC6A2B71050055793B4679F08CA725CDCA1F4792CCB566494D8F4C69808010494499E469C289BA7B9E2720152EC0130004320FC1D8420008647E8230726FDFED6E6A401564EBA6002FD3417350D7C28400C8C8600A5003EB22413BED673AB8EC95ED0CE5D480285C00372755E11CCFB164920070B40118DB1AE5901C0199DCD8D616CFA89009BF600880021304E0EC52100623A4648AB33EB51BCC017C0040E490A490A532F86016CA064E2B4939CEABC99F9009632FDE3AE00660200D4398CD120401F8C70DE2DB004A9296C662750663EC89C1006AF34B9A00BCFDBB4BBFCB5FBFF98980273B5BD37FCC4DF00354100762EC258C6000854158750A2072001F9338AC05A1E800535230DDE318597E61567D88C013A00C2A63D5843D80A958FBBBF5F46F2947F952D7003E5E1AC4A854400404A069802B25618E008667B7BAFEF24A9DD024F72DBAAFCB312002A9336C20CE84'

# Mapinha simples pra transformar hexadecimal em binário
map_hex_bin = {
    '0':'0000',
    '1':'0001',
    '2':'0010',
    '3':'0011',
    '4':'0100',
    '5':'0101',
    '6':'0110',
    '7':'0111',
    '8':'1000',
    '9':'1001',
    'A':'1010',
    'B':'1011',
    'C':'1100',
    'D':'1101',
    'E':'1110',
    'F':'1111'
}

# Convertendo hexadecimal em binário
data_bin = ""
for h in data_hex:
    data_bin += map_hex_bin[h]

print(data_bin)

# Função recursiva que analiza os pacotes e acumula versões. O último parâmetro indica se vamos continuar ou parar quando termina um pacote.
def parse_packet(bdata, blen, keep_parsing):
    pos, value = 0, 0
    while(pos < blen-6): # tem que caber pelo menos o packet version e o packet id
        # Lendo packet Version
        version = int( bdata[pos:pos+3], 2 )
        print(version)
        pos += 3
        # Lendo packet ID
        id = int( bdata[pos:pos+3], 2 )
        pos += 3
        # Literal
        if( id == 4 ):
            lit_bin = ''
            while(True):
                flag_last = int(bdata[pos:pos+1],2)
                pos += 1
                nibble = bdata[pos:pos+4]
                pos += 4
                lit_bin += nibble
                if( flag_last == 0 ):
                    break
            value = int(lit_bin,2)

        # Se não é literal, é operator
        elif( id == 0 ): # soma dos subpackets
            value = 0
            length_type = int(bdata[pos:pos+1],2)
            pos += 1
            if( length_type == 0): # length ocupa os próximos 15 bits
                lensub = int(bdata[pos:pos+15],2)
                pos += 15
                # Agora vamos analizar pelo tamanho que ocupa os subpackets
                while(lensub > 0):
                    dpos, dvalue = parse_packet(bdata[pos:pos+lensub], lensub, True)
                    pos += dpos
                    value += dvalue
                    lensub -= dpos
            else: # número de sub-packets ocupa os próximos 11 bits
                numsub = int(bdata[pos:pos+11],2)
                pos += 11
                # Analisando pela quantidade de subpackets
                for s in range(numsub):
                    dpos, dvalue = parse_packet(bdata[pos:], blen-pos, False)
                    pos += dpos
                    value += dvalue

        elif( id == 1 ): # produto dos subpackets
            value = 1 # Então, o elemento neutro é 1
            length_type = int(bdata[pos:pos+1],2)
            pos += 1
            if( length_type == 0): # length ocupa os próximos 15 bits
                lensub = int(bdata[pos:pos+15],2)
                pos += 15
                # Agora vamos analizar pelo tamanho que ocupa os subpackets
                while(lensub > 0):
                    dpos, dvalue = parse_packet(bdata[pos:pos+lensub], lensub, True)
                    pos += dpos
                    value *= dvalue
                    lensub -= dpos
            else: # número de sub-packets ocupa os próximos 11 bits
                numsub = int(bdata[pos:pos+11],2)
                pos += 11
                # Analisando pela quantidade de subpackets
                for s in range(numsub):
                    dpos, dvalue = parse_packet(bdata[pos:], blen-pos, False)
                    pos += dpos
                    value *= dvalue

        elif( id == 2 ): # valor mínimo dos subpackets
            value = None
            length_type = int(bdata[pos:pos+1],2)
            pos += 1
            if( length_type == 0): # length ocupa os próximos 15 bits
                lensub = int(bdata[pos:pos+15],2)
                pos += 15
                # Agora vamos analizar pelo tamanho que ocupa os subpackets
                while(lensub > 0):
                    dpos, dvalue = parse_packet(bdata[pos:pos+lensub], lensub, True)
                    pos += dpos
                    if( value == None or value > dvalue ):
                        value = dvalue
                    lensub -= dpos
            else: # número de sub-packets ocupa os próximos 11 bits
                numsub = int(bdata[pos:pos+11],2)
                pos += 11
                # Analisando pela quantidade de subpackets
                for s in range(numsub):
                    dpos, dvalue = parse_packet(bdata[pos:], blen-pos, False)
                    pos += dpos
                    if( value == None or value > dvalue ):
                        value = dvalue

        elif( id == 3 ): # valor máximo dos subpackets
            value = None
            length_type = int(bdata[pos:pos+1],2)
            pos += 1
            if( length_type == 0): # length ocupa os próximos 15 bits
                lensub = int(bdata[pos:pos+15],2)
                pos += 15
                # Agora vamos analizar pelo tamanho que ocupa os subpackets
                while(lensub > 0):
                    dpos, dvalue = parse_packet(bdata[pos:pos+lensub], lensub, True)
                    pos += dpos
                    if( value == None or value < dvalue ):
                        value = dvalue
                    lensub -= dpos
            else: # número de sub-packets ocupa os próximos 11 bits
                numsub = int(bdata[pos:pos+11],2)
                pos += 11
                # Analisando pela quantidade de subpackets
                for s in range(numsub):
                    dpos, dvalue = parse_packet(bdata[pos:], blen-pos, False)
                    pos += dpos
                    if( value == None or value > dvalue ):
                        value = dvalue

        elif( id == 5 ): # "maior que". Sempre tem 2 subpackets para comparar.
            length_type = int(bdata[pos:pos+1],2)
            pos += 1
            if( length_type == 0): # length ocupa os próximos 15 bits
                lensub = int(bdata[pos:pos+15],2)
                pos += 15
                # Agora vamos analizar pelo tamanho que ocupa os subpackets
                dpos, v1 = parse_packet(bdata[pos:pos+lensub], lensub, True)
                pos += dpos
                lensub -= dpos
                dpos, v2 = parse_packet(bdata[pos:pos+lensub], lensub, True)
                pos += dpos
                lensub -= dpos
                if( v1 > v2 ):
                    value = 1
                else:
                    value = 0

            else: # número de sub-packets ocupa os próximos 11 bits
                numsub = int(bdata[pos:pos+11],2)
                pos += 11
                dpos, v1 = parse_packet(bdata[pos:], blen-pos, False)
                pos += dpos
                dpos, v2 = parse_packet(bdata[pos:], blen-pos, False)
                pos += dpos
                if( v1 > v2 ):
                    value = 1
                else:
                    value = 0
                    
        elif( id == 6 ): # "menor que". Sempre tem 2 subpackets para comparar.
            length_type = int(bdata[pos:pos+1],2)
            pos += 1
            if( length_type == 0): # length ocupa os próximos 15 bits
                lensub = int(bdata[pos:pos+15],2)
                pos += 15
                # Agora vamos analizar pelo tamanho que ocupa os subpackets
                dpos, v1 = parse_packet(bdata[pos:pos+lensub], lensub, True)
                pos += dpos
                lensub -= dpos
                dpos, v2 = parse_packet(bdata[pos:pos+lensub], lensub, True)
                pos += dpos
                lensub -= dpos
                if( v1 < v2 ):
                    value = 1
                else:
                    value = 0

            else: # número de sub-packets ocupa os próximos 11 bits
                numsub = int(bdata[pos:pos+11],2)
                pos += 11
                dpos, v1 = parse_packet(bdata[pos:], blen-pos, False)
                pos += dpos
                dpos, v2 = parse_packet(bdata[pos:], blen-pos, False)
                pos += dpos
                if( v1 < v2 ):
                    value = 1
                else:
                    value = 0
        elif( id == 7 ): # "igual a". Sempre tem 2 subpackets para comparar.
            length_type = int(bdata[pos:pos+1],2)
            pos += 1
            if( length_type == 0): # length ocupa os próximos 15 bits
                lensub = int(bdata[pos:pos+15],2)
                pos += 15
                # Agora vamos analizar pelo tamanho que ocupa os subpackets
                dpos, v1 = parse_packet(bdata[pos:pos+lensub], lensub, True)
                pos += dpos
                lensub -= dpos
                dpos, v2 = parse_packet(bdata[pos:pos+lensub], lensub, True)
                pos += dpos
                lensub -= dpos
                if( v1 == v2 ):
                    value = 1
                else:
                    value = 0

            else: # número de sub-packets ocupa os próximos 11 bits
                numsub = int(bdata[pos:pos+11],2)
                pos += 11
                dpos, v1 = parse_packet(bdata[pos:], blen-pos, False)
                pos += dpos
                dpos, v2 = parse_packet(bdata[pos:], blen-pos, False)
                pos += dpos
                if( v1 == v2 ):
                    value = 1
                else:
                    value = 0
        # Se for para pararmos de analizar após achar 1 pacote
        if( not keep_parsing ):
            break
    return pos, value

# Analizando o pacote inteiro, ele deve ser um pacotão único
pos, value = parse_packet(data_bin, len(data_bin), False)

print(value)