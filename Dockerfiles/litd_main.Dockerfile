FROM litd_base_image




# add user
ARG UNAME=litd
ARG UID=1000
ARG GID=1000

# note, alpine has different commands needed
RUN addgroup -g $GID $UNAME
RUN adduser -D -u $UID -G $UNAME $UNAME






CMD [   \
#      "litd", \

      "--disableui", \
      "--macaroonpath=/home/litd/.lit/regtest/lit.macaroon", \

      "--lnd.bitcoind.rpchost=172.99.0.2:18443", \
      "--lnd.bitcoind.zmqpubrawtx=tcp://172.99.0.2:28335", \
      "--lnd.bitcoind.zmqpubrawblock=tcp://172.99.0.2:28334", \

      "--lnd.bitcoind.rpcuser=polaruser", \
      "--lnd.bitcoind.rpcpass=polaruser", \
      "--lnd.bitcoin.regtest", \
      "--lnd.bitcoin.node=bitcoind", \
      "--lnd-mode=integrated", \


      "--httpslisten=0.0.0.0:8443", \
      "--network=regtest", \
      "--pool-mode=disable", \
      "--loop-mode=disable", \
      "--autopilot.disable", \

      "--lnd.noseedbackup", \
      "--lnd.debuglevel=debug", \
      "--taproot-assets.allow-public-uni-proof-courier", \
      "--taproot-assets.universe.public-access=rw", \
      "--taproot-assets.universe.sync-all-assets", \
      "--taproot-assets.allow-public-stats", \
      "--taproot-assets.universerpccourier.skipinitdelay", \
      "--taproot-assets.universerpccourier.backoffresetwait=1s", \
      "--taproot-assets.universerpccourier.numtries=5", \
      "--taproot-assets.universerpccourier.initialbackoff=300ms", \
      "--taproot-assets.universerpccourier.maxbackoff=600ms", \
      "--taproot-assets.experimental.rfq.priceoracleaddress=use_mock_price_oracle_service_promise_to_not_use_on_mainnet", \
      "--taproot-assets.experimental.rfq.mockoracleassetsperbtc=1000000", \
      "--lnd.trickledelay=50", \
      "--lnd.gossip.sub-batch-delay=5ms", \
      "--lnd.caches.rpc-graph-cache-duration=100ms", \
      "--lnd.default-remote-max-htlcs=483", \
      "--lnd.dust-threshold=5000000", \
      "--lnd.protocol.option-scid-alias", \
      "--lnd.protocol.zero-conf", \
      "--lnd.protocol.simple-taproot-chans", \
      "--lnd.protocol.simple-taproot-overlay-chans", \
      "--lnd.protocol.wumbo-channels", \
      "--lnd.accept-keysend", \
      "--lnd.protocol.custom-message=17" \

# note, can't have a ',' on the final line!

    ]


