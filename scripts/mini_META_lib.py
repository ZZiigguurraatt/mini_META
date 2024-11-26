

from lndgrpc import LNDClient
from yaml import safe_load
import bitcoin.rpc


bitcoindHost='http://polaruser:polaruser@172.99.0.2:18443'




# get the name and settings (mainly just the IP address) for each node

with open('/mini_META/docker-compose.yaml', 'r') as file:
    network_info=safe_load(file)

litd_nodes=network_info['services']     #should change this to do a copy instead?

# remove other nodes from the list
litd_nodes.pop('bitcoind')
litd_nodes.pop('litd_base')
litd_nodes.pop('litd_main')
litd_nodes.pop('controller')

print("total nodes: "+str(len(litd_nodes.keys())))
print()

def initNode(node_name, node_config):
    """create an object for the node"""
    nodeObject={}
    nodeObject['lnd']=LNDClient(host=node_config['networks']['mini_META_net']['ipv4_address']+':8443',cert_filepath='/mini_META/net_data/'+node_name+'/.lit/tls.cert',macaroon_filepath='/mini_META/net_data/'+node_name+'/.lnd/data/chain/bitcoin/regtest/admin.macaroon')
    nodeObject['tapd']=LNDClient(host=node_config['networks']['mini_META_net']['ipv4_address']+':8443',cert_filepath='/mini_META/net_data/'+node_name+'/.lit/tls.cert',macaroon_filepath='/mini_META/net_data/'+node_name+'/.tapd/data/regtest/admin.macaroon')
    return nodeObject



# create an object for connecting to every node
litd_node_objects={}
for node_name, node_config in litd_nodes.items():
    litd_node_objects[node_name]=initNode(node_name, node_config)



def SendAssetToFro(receiver,sender,amount,TheAssetID):

    print(sender+' sending '+ str(amount)+' of '+TheAssetID.hex()+' to '+receiver+' on chain')

    TheAssetAddress=litd_node_objects[receiver]['tapd'].new_addr(asset_id=TheAssetID,amt=amount).encoded
    litd_node_objects[sender]['tapd'].send_asset(tap_addrs=[TheAssetAddress,])

    # mine some more blocks
    MiningAddress=bitcoin.rpc.RawProxy(service_url=bitcoindHost).getnewaddress()
    bitcoin.rpc.RawProxy(service_url=bitcoindHost).generatetoaddress(10,MiningAddress)



def OpenTaprootAssetChannel(funder,peer,AssetID):
    '''open a taproot asset channels'''

    print(funder+' funding a '+AssetID.hex()+' channel with '+peer)

    #if this messes up, need to abandon channels on both peers
#change fund_taprootasset_channel to accept hex like open_channel?????
    litd_node_objects[funder]['tapd'].fund_taprootasset_channel(asset_amount=200, asset_id=AssetID, peer_pubkey=bytes.fromhex(litd_node_objects[peer]['lnd'].get_info().identity_pubkey), fee_rate_sat_per_vbyte=10)

    # mine some more blocks
    MiningAddress=bitcoin.rpc.RawProxy(service_url=bitcoindHost).getnewaddress()
    bitcoin.rpc.RawProxy(service_url=bitcoindHost).generatetoaddress(10,MiningAddress)

    return



def OpenRegularChannel(funder,peer):
    '''open a regular channels'''

    print(funder+' funding a normal sats channel with '+peer)

    litd_node_objects[funder]['lnd'].open_channel(node_pubkey=litd_node_objects[peer]['lnd'].get_info().identity_pubkey, local_funding_amount=50000, sat_per_byte=10)

    # mine some more blocks
    MiningAddress=bitcoin.rpc.RawProxy(service_url=bitcoindHost).getnewaddress()
    bitcoin.rpc.RawProxy(service_url=bitcoindHost).generatetoaddress(10,MiningAddress)

    return




def SendTaprootAssetReceiveTaprootAsset(sender,firstHop,lastHop,receiver,amount,TheAsset):

    print('=======================================================================================')
    print(sender+' sending '+str(amount)+' of '+TheAsset.hex()+' via '+firstHop+' and '+receiver+' receiving '+TheAsset.hex()+' via '+lastHop)
    print('=======================================================================================')

    # seems to need the pubkey if two channels of the same asset even if both channels are to the same peer
    TheInvoice=litd_node_objects[receiver]['tapd'].add_taprootasset_invoice(asset_id=TheAsset,asset_amount=amount,peer_pubkey=bytes.fromhex(litd_node_objects[lastHop]['lnd'].get_info().identity_pubkey))
    TheInvoice_raw=TheInvoice.invoice_result.payment_request

    # seems to need the pubkey if two channels of the same asset even if both are the same peer
    ThePaymentResponse=litd_node_objects[sender]['tapd'].send_taprootasset_payment(asset_id=TheAsset,payment_request=TheInvoice_raw,timeout_seconds=25,peer_pubkey=bytes.fromhex(litd_node_objects[firstHop]['lnd'].get_info().identity_pubkey))

    for response in ThePaymentResponse:
        print(response)



def SendTaprootAssetReceiveSats(sender,firstHop,receiver,amount,TheAsset):

    print('=======================================================================================')
    print(sender+' sending '+str(amount)+' of '+TheAsset.hex()+' via '+firstHop+' and '+receiver+' receiving sats')
    print('=======================================================================================')

    TheInvoice=litd_node_objects[receiver]['lnd'].add_invoice(amount)
    TheInvoice_raw=TheInvoice.payment_request

    # seems to need the pubkey if two channels of the same asset even if both are the same peer
    ThePaymentResponse=litd_node_objects[sender]['tapd'].send_taprootasset_payment(asset_id=TheAsset,payment_request=TheInvoice_raw,timeout_seconds=25,peer_pubkey=bytes.fromhex(litd_node_objects[firstHop]['lnd'].get_info().identity_pubkey))

    for response in ThePaymentResponse:
        print(response)



def SendSatsReceiveTaprootAsset(sender,lastHop,receiver,amount,TheAsset):

    print('=======================================================================================')
    print(sender+' sending '+str(amount)+' sats and '+receiver+' receiving '+TheAsset.hex()+' via '+lastHop)
    print('=======================================================================================')

    # seems to need the pubkey if two channels of the same asset even if both channels are to the same peer
    TheInvoice=litd_node_objects[receiver]['tapd'].add_taprootasset_invoice(asset_id=TheAsset,asset_amount=amount,peer_pubkey=bytes.fromhex(litd_node_objects[lastHop]['lnd'].get_info().identity_pubkey))
    TheInvoice_raw=TheInvoice.invoice_result.payment_request

    # seems to need the pubkey if two channels of the same asset even if both are the same peer
    ThePaymentResponse=litd_node_objects[sender]['lnd'].send_payment_v2(payment_request=TheInvoice_raw, fee_limit_sat=10, timeout_seconds=25)

    for response in ThePaymentResponse:
        print(response)
















