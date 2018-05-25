import pywaves as py
import math

py.setNode('https://sg.katalystcoin.com')

token = py.Asset('GQsFCrD43pHkhdvt5PnZ4W9Qgg8X9LjCSWAUG6mLoFMg') #dioncoin
myAddress = py.Address(privateKey='6QsHMXahBHQmaYjA2PMDR3BFXRyWWHCAJfVMn7dWXPrk')
#myAddress = py.Address(privateKey='6QsHMXahBHQmaYjA2PMDR3BFXRyWWHCAJfVMn7dWXPrk')
#myAddress.sendAsset(recipient = py.Address(privateKey='7VkCrrhhueZTRiwwdBZ8R4DS82M3qTFGXVb8JxXhtRCg'), asset = token, amount = 100)

wallets = []

def initialiseWallets():
    wallets.append(py.Address(seed='marble cram defense virus deal hurry bread theme anchor plate brief chicken head more apple'))
    wallets.append(py.Address(seed='defy high smart genre abstract biology fantasy seat bread umbrella frost suffer manual sort three'))
    wallets.append(py.Address(seed='spray wall equip trophy awful clean write jealous tribe flash timber drum depend alone coral'))
    wallets.append(py.Address(seed='protect public thing guard describe fan once summer dignity media boil day notice harbor stay'))
    wallets.append(py.Address(seed='main cart invest soldier enact pill eight fame shallow say level scrap drift charge direct'))
    wallets.append(py.Address(seed='bundle employ mesh region vibrant broccoli armed rubber sing danger snake casual ability page twist'))
    wallets.append(py.Address(seed='only decade fine upset skull thought weasel cause miss cheese side build blur manage proof'))
    wallets.append(py.Address(seed='plunge draw hedgehog chief jeans narrow flight abuse isolate amazing mirror advance bone crucial educate'))
    wallets.append(py.Address(seed='bean tool all make clap disagree food buyer forward toy find miracle sick sauce slide'))
    wallets.append(py.Address(seed='fresh return verb source radio response broom space appear way energy owner polar electric lock'))



initialiseWallets()

#print(wallets)

height = py.height()
value = 25 * math.pow(10, 8)

myAddress.sendAsset(recipient=wallets[0], asset=token, amount=value)

while True:
    currentHeight = py.height()

    if (currentHeight == (height + 1)):
        height += 1
        print("----------------------")
        print(height)
        for i in range(0, 10):
            walletAddress = wallets[i]
            
            myAddress.sendAsset(recipient=walletAddress, asset=token, amount=value)

        print(wallets)





            

            
    
    
