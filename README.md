# Internet Computer Node Provider Self-Declarations

This repository is the public home of the **self-declarations** and supporting
documents of Internet Computer node providers.

A prospective node provider publishes their self-declaration and supporting
artefacts here, and then references those files and their SHA-256 hashes in their
NNS node-provider registration proposal. Anyone can re-compute the hashes from
this repository and compare them with the hashes in the proposal.

This replaces the retired `wiki.internetcomputer.org` wiki, which previously
hosted these documents. The declarations that were on the wiki have been
backfilled here.

> **Note:** Reviewers of this repository check that a submission is complete,
> correctly named and free of harmful content. They do **not** verify or vouch
> for the truthfulness of the statements a node provider makes in their
> declaration. A declaration might separately be reviewed by an auditor, who
> requests supporting documents privately — see
> [CONTRIBUTING.md](CONTRIBUTING.md#private-disclosure-for-a-potential-audit).

## Why node providers self-declare

The Network Nervous System is committed to the principles of decentralization to
enhance the overall security and reliability of the ICP network. Moreover, node
machines must not be funded or controlled by criminal entities, as these critical
infrastructure components form the foundation upon which the integrity of the
entire ecosystem depends. To achieve these goals, comprehensive disclosures from
node providers are required. In particular, node providers are required to:

- confirm their identity;
- commit to providing the required hardware and honest operations, as specified
  in the ICP Network guidelines;
- confirm lawful source of funds and source of wealth;
- assess potential overlaps with other node providers.

As part of the governance structure, the Network Nervous System may vote to:

- remove node providers that violate these principles or provide untruthful
  responses;
- appoint legal representation to pursue such node providers.

## What the self-declaration covers

The form in
[templates/node-provider-self-declaration.md](templates/node-provider-self-declaration.md)
has two parts:

- **Identity and compliance declarations** — the statement of identity (A), the
  guarantee to provide node machines per the required hardware configuration (B),
  the statement of good intent (C), and the confirmation of a lawful source of
  funds and wealth (D).
- **Assessment of independence** — ultimate beneficial ownership and control
  (Q1), and any overlap with other node providers through common owners (Q2),
  family ties (Q3), corporate structure (Q4) or financing (Q5).

Everything a node provider writes into the form is **public**: it is published in
this repository. The evidence that backs those statements up — corporate records,
IDs, bank statements, hardware receipts — is **private**: it is shared only with
an auditor, if one is assigned, and is never committed here. See
[CONTRIBUTING.md](CONTRIBUTING.md#private-disclosure-for-a-potential-audit) for
what that evidence consists of.

## Repository layout

```
├── README.md                       # this file: intro, index, how to submit
├── CONTRIBUTING.md                 # step-by-step submission guide
├── CODEOWNERS                      # who must approve a pull request
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md    # the submission checklist
│   └── workflows/validate.yml      # blocking PR checks
├── scripts/validate.py             # the checks, runnable locally
├── templates/                      # copy these into your own directory
└── node-providers/                 # one directory per node provider
    └── <provider-slug>/
        ├── README.md               # identity, principal, document manifest
        ├── <provider-slug>-self-declaration.pdf
        └── <provider-slug>-proof-of-identity.pdf
```

## What every node provider must submit

| Document | Required | Doc-type in file name |
| --- | --- | --- |
| Per-provider README with the document manifest | yes | — (`README.md`) |
| Self-declaration | yes | `self-declaration` |
| Proof of identity (e.g. commercial-register extract) | yes | `proof-of-identity` |
| Excess-node handover statement | optional | `excess-node-handover` |
| Proof of hardware order | optional | `proof-of-hardware-order` |
| Auditor confirmation letter | optional | `auditor-confirmation` |
| Addendum to a declaration | optional | `addendum` |

### Naming convention

Every document is named:

```
<provider-slug>-<doc-type>.<ext>
```

- `<provider-slug>` — lowercase kebab-case, identical to the directory name;
- `<doc-type>` — one of `self-declaration`, `proof-of-identity`,
  `excess-node-handover`, `proof-of-hardware-order`, `addendum`,
  `auditor-confirmation`;
- `<ext>` — `pdf` is preferred for signed documents (`md`, `png`, `jpg` are also
  accepted).

File names carry no date; the date of each document is recorded in the manifest.
If a provider has more than one document of the same doc-type, the second and
further ones get a numeric suffix: `<provider-slug>-<doc-type>-2.<ext>`.

## How to submit

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full walk-through. In short:

1. Fork this repository and create `node-providers/<your-slug>/`.
2. Copy the files from [templates/](templates/) into it and fill them in.
3. Add your signed documents, named per the convention above.
4. List every file with its SHA-256 hash in your `README.md` manifest.
5. Run `python3 scripts/validate.py --all` and open a pull request.

## Verifying a declaration

To check that the documents in a provider directory are the ones referenced in
the NNS proposal:

```sh
cd node-providers/<provider-slug>
shasum -a 256 *          # macOS
sha256sum *              # Linux
```

Compare the output with the manifest in that directory's `README.md` and with
the hashes in the NNS registration proposal linked from it.

## Index of node providers

The 101 node providers below were backfilled from the retired wiki on
2026-07-30 and matched to their on-chain registration proposals. `none` means the
provider was registered before node-provider onboarding moved to NNS proposals.

`example-provider-llc/` is a template example, not a node provider.

| Node provider | Directory | Principal | NNS proposal |
| --- | --- | --- | --- |
| 0X52 | [0x52](node-providers/0x52/) | `2wxzd-qrbrs-ailta-kdtyb-ucg35-xcxd4-txevb-ot7hx-wiyus-szcca-nqe` | [135172](https://dashboard.internetcomputer.org/proposal/135172) |
| 100 Count Holdings, LLC | [100-count-holdings-llc](node-providers/100-count-holdings-llc/) | `2dgp4-h57n4-a4kgx-n4uun-huo3a-wbdlc-m57wd-jtkuh-g5vcc-fcbby-6qe` | [135264](https://dashboard.internetcomputer.org/proposal/135264) |
| 43rd Big Idea Films | [43rd-big-idea-films](node-providers/43rd-big-idea-films/) | `sqhxa-h6ili-qkwup-ohzwn-yofnm-vvnp5-kxdhg-saabw-rvua3-xp325-zqe` | none |
| 87m Neuron, LLC | [87m-neuron-llc](node-providers/87m-neuron-llc/) | `eipr5-izbom-neyqh-s3ec2-52eww-cyfpg-qfomg-3dpwj-4pffh-34xcu-7qe` | [46915](https://dashboard.internetcomputer.org/proposal/46915) |
| ACCUSET SOLUTIONS | [accuset-solutions](node-providers/accuset-solutions/) | `cp5ib-twnmx-h4dvd-isef2-tu44u-kb2ka-fise5-m4hta-hnxoq-k45mm-hqe` | [123944](https://dashboard.internetcomputer.org/proposal/123944) |
| achermann.swiss | [achermann-swiss](node-providers/achermann-swiss/) | `gjsts-tuec7-wp6cl-zmk6w-sfpp6-ei34c-l7njq-les4c-yupv3-hbcpg-tae` | [138365](https://dashboard.internetcomputer.org/proposal/138365) |
| Aitubi AG | [aitubi-ag](node-providers/aitubi-ag/) | `znw2p-4cx6u-ocqls-277iu-2lkir-xjy7g-4s3sj-sjy6j-mtlay-rnnra-yqe` | [128809](https://dashboard.internetcomputer.org/proposal/128809) |
| Allusion | [allusion](node-providers/allusion/) | `rbn2y-6vfsb-gv35j-4cyvy-pzbdu-e5aum-jzjg6-5b4n5-vuguf-ycubq-zae` | none |
| AlpineDC SA | [alpinedc-sa](node-providers/alpinedc-sa/) | `mrfhx-rsvqz-jndwd-3nrkb-fw3wy-cq64z-iszxt-drffc-f4rtj-ivoop-6ae` | [138081](https://dashboard.internetcomputer.org/proposal/138081) |
| Anonstake | [anonstake](node-providers/anonstake/) | `kos24-5xact-6aror-uofg2-tnvt6-dq3bk-c2c5z-jtptt-jbqvc-lmegy-qae` | [107568](https://dashboard.internetcomputer.org/proposal/107568) |
| ANTHONY ISAAKIDIS | [anthony-isaakidis](node-providers/anthony-isaakidis/) | `dnpkk-x67ir-zwcyz-fkgzz-547t7-papxf-zby5t-i2log-uodsf-pcizd-jae` | [136590](https://dashboard.internetcomputer.org/proposal/136590) |
| ANYPOINT PTY LTD | [anypoint-pty-ltd](node-providers/anypoint-pty-ltd/) | `fwnmn-zn7yt-5jaia-fkxlr-dzwyu-keguq-npfxq-mc72w-exeae-n5thj-oae` | [124029](https://dashboard.internetcomputer.org/proposal/124029) |
| Arceau NP LLC | [arceau-np-llc](node-providers/arceau-np-llc/) | `ss6oe-fm7b2-b5r57-y3x74-omrz5-d5pgy-5iwtw-4aew5-aqj3l-6ydra-wqe` | [135032](https://dashboard.internetcomputer.org/proposal/135032) |
| Artem Horodyskyi | [artem-horodyskyi](node-providers/artem-horodyskyi/) | `diyay-s4rfq-xnx23-zczwi-nptra-5254n-e4zn6-p7tqe-vqhzr-sd4gd-bqe` | [126003](https://dashboard.internetcomputer.org/proposal/126003) |
| Aspire Properties | [aspire-properties](node-providers/aspire-properties/) | `2byzn-q2crt-hgczo-eruff-6p7af-pemor-n2z4z-6d2sd-wvdqa-yqvxb-mqe` | [123020](https://dashboard.internetcomputer.org/proposal/123020) |
| Avalution AG | [avalution-ag](node-providers/avalution-ag/) | `is2tg-4for6-ytyzl-5xokl-jd3kz-4y5ky-g7am2-yotrq-5yruf-twke6-vae` | [138265](https://dashboard.internetcomputer.org/proposal/138265) |
| AVRVM AG | [avrvm-ag](node-providers/avrvm-ag/) | `33aps-ovxje-mwpux-cy2hh-f2qwp-5tzxs-2edbb-gblfn-ev5pv-cfnvj-pqe` | [126117](https://dashboard.internetcomputer.org/proposal/126117) |
| Bianca-Martina Rohner | [bianca-martina-rohner](node-providers/bianca-martina-rohner/) | `eatbv-nlydd-n655c-g7j7p-gnmpz-pszdg-6e6et-veobv-ftz2y-4m752-vqe` | [126367](https://dashboard.internetcomputer.org/proposal/126367) |
| Bigger Capital | [bigger-capital](node-providers/bigger-capital/) | `7a4u2-gevsy-5c5fs-hsgri-n2kdz-dxxwf-btcfp-jykro-l4y7c-7xky2-aqe` | none |
| Bitmoon | [bitmoon](node-providers/bitmoon/) | `mjnyf-lzqq6-s7fzb-62rqm-xzvge-5oa26-humwp-dvwxp-jxxkf-hoel7-fqe` | [125574](https://dashboard.internetcomputer.org/proposal/125574) |
| Blockchain Development Labs | [blockchain-development-labs](node-providers/blockchain-development-labs/) | `7at4h-nhtvt-a4s55-jigss-wr2ha-ysxkn-e6w7x-7ggnm-qd3d5-ry66r-cae` | [7909](https://dashboard.internetcomputer.org/proposal/7909) |
| Blockchain Innovation Group | [blockchain-innovation-group](node-providers/blockchain-innovation-group/) | `c3i3u-4ot4i-zino3-jrxre-7s426-dk2th-cvino-nznco-lkbpn-vl5of-4qe` | [138355](https://dashboard.internetcomputer.org/proposal/138355) |
| BlockFinance | [blockfinance](node-providers/blockfinance/) | `c5svp-7pkmf-agz5x-536k7-r7rcw-4wn3a-eo7pt-ry7su-j42uq-bvnzf-iqe` | [135199](https://dashboard.internetcomputer.org/proposal/135199) |
| BlockTech Ventures, LLC | [blocktech-ventures-llc](node-providers/blocktech-ventures-llc/) | `ks7ow-zvs7i-ratdk-azq34-zio2b-gbekj-qjicg-pfhp3-ovhgu-k5qql-dae` | none |
| BLP22, LLC | [blp22-llc](node-providers/blp22-llc/) | `sma3p-ivkif-hz7nu-ngmvq-ibnjg-nubke-zf6gh-wbnfc-2dlng-l3die-zqe` | none |
| Blue Ant LLC | [blue-ant-llc](node-providers/blue-ant-llc/) | `rpfvr-s3kuw-xdqrr-pvuuj-hc7hl-olytw-yxlie-fmr74-sr572-6gdqx-iqe` | [134721](https://dashboard.internetcomputer.org/proposal/134721) |
| Bohatyrov Volodymyr | [bohatyrov-volodymyr](node-providers/bohatyrov-volodymyr/) | `dhywe-eouw6-hstpj-ahsnw-xnjxq-cmqks-47mrg-nnncb-3sr5d-rac6m-nae` | [125632](https://dashboard.internetcomputer.org/proposal/125632) |
| Buldakova Rehina | [buldakova-rehina](node-providers/buldakova-rehina/) | `qipsq-44ztq-4oxob-dulxs-35tho-zjf5o-onu2b-sjuhk-4jd7x-yfdhz-qae` | [126846](https://dashboard.internetcomputer.org/proposal/126846) |
| Carbon Twelve | [carbon-twelve](node-providers/carbon-twelve/) | `qsdw4-ao5ye-6rtq4-y3zhm-icjbj-lutd2-sbejz-4ajqz-pcflr-xrhsg-jae` | [126317](https://dashboard.internetcomputer.org/proposal/126317) |
| Conic Ventures | [conic-ventures](node-providers/conic-ventures/) | `i3cfo-s2tgu-qe5ym-wk7e6-y7ura-pptgu-kevuf-2feh7-z4enq-5hz4s-mqe` | [124554](https://dashboard.internetcomputer.org/proposal/124554) |
| Coplus Limited | [coplus-limited](node-providers/coplus-limited/) | `jz47c-irtey-dr2nb-wienh-emhaz-jo6ua-gsbho-t2z5j-l7kbf-5i7p5-5ae` | [124024](https://dashboard.internetcomputer.org/proposal/124024) |
| CoreLedger | [coreledger](node-providers/coreledger/) | `g4gfo-2buho-hg3ho-pamsx-yg2vz-qnz2r-fsn65-j6dv7-myful-iy6vv-tqe` | [138314](https://dashboard.internetcomputer.org/proposal/138314) |
| Decentralized | [decentralized](node-providers/decentralized/) | `hokzb-gsg3k-oj44m-tqnhs-mpmwl-ujv4x-44bsz-gdoce-pl6tv-oin7v-eae` | [138905](https://dashboard.internetcomputer.org/proposal/138905) |
| Decentralized Entities Foundation | [decentralized-entities-foundation](node-providers/decentralized-entities-foundation/) | `w4buy-lgwzr-pccs7-huzhh-qqnws-rns75-iaoox-jolrm-xs2ra-vdu3o-2qe` | [134015](https://dashboard.internetcomputer.org/proposal/134015) |
| DFINITY Stiftung | [dfinity-stiftung](node-providers/dfinity-stiftung/) | `bvcsg-3od6r-jnydw-eysln-aql7w-td5zn-ay5m6-sibd2-jzojt-anwag-mqe` | none |
| Eastman Ventures (Pty) Ltd | [eastman-ventures-pty-ltd](node-providers/eastman-ventures-pty-ltd/) | `veamq-6zmtx-dtdky-ctoun-gokvu-cr6zm-ffsky-dz35w-e2euw-zvv7e-vae` | [126329](https://dashboard.internetcomputer.org/proposal/126329) |
| Exaion | [exaion](node-providers/exaion/) | `xo7ih-nswlt-hbq3n-v5ixi-etu7j-sasg6-fjf4p-zx6or-cc7c3-pnh7t-2ae` | [120149](https://dashboard.internetcomputer.org/proposal/120149) |
| Extragone SA | [extragone-sa](node-providers/extragone-sa/) | `7ryes-jnj73-bsyu4-lo6h7-lbxk5-x4ien-lylws-5qwzl-hxd5f-xjh3w-mqe` | none |
| Ferndale International | [ferndale-international](node-providers/ferndale-international/) | `34cav-6s7rb-uwa3c-awdly-5md4r-lwueh-atzbn-unqpe-c5ope-f3nqj-wae` | [128800](https://dashboard.internetcomputer.org/proposal/128800) |
| Fractal Labs AG | [fractal-labs-ag](node-providers/fractal-labs-ag/) | `wdjjk-blh44-lxm74-ojj43-rvgf4-j5rie-nm6xs-xvnuv-j3ptn-25t4v-6ae` | none |
| Geeta Kalwani | [geeta-kalwani](node-providers/geeta-kalwani/) | `otzuu-dldzs-avvu2-qwowd-hdj73-aocy7-lacgi-carzj-m6f2r-ffluy-fae` | [126403](https://dashboard.internetcomputer.org/proposal/126403) |
| Geodd Pvt Ltd | [geodd-pvt-ltd](node-providers/geodd-pvt-ltd/) | `eybf4-6t6bb-unfb2-h2hhn-rrfi2-cd2vs-phksn-jdmbn-i463m-4lzds-vqe` | [122772](https://dashboard.internetcomputer.org/proposal/122772) |
| GeoNodes LLC | [geonodes-llc](node-providers/geonodes-llc/) | `6sq7t-knkul-fko6h-xzvnf-ktbvr-jhx7r-hapzr-kjlek-whugy-zt6ip-xqe` | [126860](https://dashboard.internetcomputer.org/proposal/126860) |
| George Bassadone | [george-bassadone](node-providers/george-bassadone/) | `vegae-c4chr-aetfj-7gzuh-c23sx-u2paz-vmvbn-bcage-pu7lu-mptnn-eqe` | [126844](https://dashboard.internetcomputer.org/proposal/126844) |
| Giant Leaf, LLC | [giant-leaf-llc](node-providers/giant-leaf-llc/) | `wwdbq-xuqhf-eydzu-oyl7p-ga565-zm7s7-yrive-ozgsy-zzgh3-qwb3j-cae` | none |
| Honeycomb Capital (Pty) Ltd | [honeycomb-capital-pty-ltd](node-providers/honeycomb-capital-pty-ltd/) | `nmdd6-rouxw-55leh-wcbkn-kejit-njvje-p4s6e-v64d3-nlbjb-vipul-mae` | [122528](https://dashboard.internetcomputer.org/proposal/122528) |
| Iancu Aurel | [iancu-aurel](node-providers/iancu-aurel/) | `i7dto-bgkj2-xo5dx-cyrb7-zkk5y-q46eh-gz6iq-qkgyc-w4qte-scgtb-6ae` | [46913](https://dashboard.internetcomputer.org/proposal/46913) |
| Icaria Systems Pty Ltd | [icaria-systems-pty-ltd](node-providers/icaria-systems-pty-ltd/) | `ihbuj-erwnc-tkjux-tqtnv-zkoar-uniy2-sk2go-xfpkc-znbb4-seukm-wqe` | [119823](https://dashboard.internetcomputer.org/proposal/119823) |
| Icswitch | [icswitch](node-providers/icswitch/) | `gtdcl-kijoz-5fk3p-acmop-gmocy-nhpeq-a5fay-7q5ol-4lmdk-ldz4m-aqe` | [137343](https://dashboard.internetcomputer.org/proposal/137343) |
| Illusions In Art (Pty) Ltd | [illusions-in-art-pty-ltd](node-providers/illusions-in-art-pty-ltd/) | `optdi-nwa4m-hly3k-6ua4n-sqyxf-yahvb-wps77-ddayn-r7zcz-edla5-7qe` | [123792](https://dashboard.internetcomputer.org/proposal/123792) |
| InfoObjects | [infoobjects](node-providers/infoobjects/) | `7ws2n-wqorv-vmo4m-5e222-n42c3-hk43s-ei3kp-4hpbn-xlkzo-jgv7i-tqe` | [98092](https://dashboard.internetcomputer.org/proposal/98092) |
| Ivanov Oleksandr | [ivanov-oleksandr](node-providers/ivanov-oleksandr/) | `ivf2y-crxj4-y6ewo-un35q-a7pum-wqmbw-pkepy-d6uew-bfmff-g5yxe-eae` | [125523](https://dashboard.internetcomputer.org/proposal/125523) |
| Karel Frank | [karel-frank](node-providers/karel-frank/) | `unqqg-no4b2-vbyad-ytik2-t3vly-3e57q-aje2t-sjb5l-bd4ke-chggn-uqe` | [115658](https://dashboard.internetcomputer.org/proposal/115658) |
| Kontrapunt (Pty) Ltd | [kontrapunt-pty-ltd](node-providers/kontrapunt-pty-ltd/) | `py2kr-ipr2p-ryh66-x3a3v-5ts6u-7rfhf-alkna-ueffh-hz5ox-lt6du-qqe` | [124775](https://dashboard.internetcomputer.org/proposal/124775) |
| Krishna Enterprises | [krishna-enterprises](node-providers/krishna-enterprises/) | `zy4m7-z5mhs-zfkpl-zlsjl-blrbx-mvvmq-5z4zu-mf7eq-hhv7o-ezfro-3ae` | [125158](https://dashboard.internetcomputer.org/proposal/125158) |
| Krzysztof Żelazko | [krzysztof-zelazko](node-providers/krzysztof-zelazko/) | `j2tnr-f5tmm-afnyl-762n7-o272x-ji2xi-bcpld-ihimy-fw52d-2zqov-xae` | [126414](https://dashboard.internetcomputer.org/proposal/126414) |
| Louise Velayo | [louise-velayo](node-providers/louise-velayo/) | `fnzev-s6xem-s2myy-rrxoa-2mpp6-oet33-pmnba-ajo75-qhfdw-esys7-7qe` | [130774](https://dashboard.internetcomputer.org/proposal/130774) |
| LTIN AG | [ltin-ag](node-providers/ltin-ag/) | `qpwbv-tu7uj-vpndf-talpd-zufus-itpe5-n66ua-yahhs-ttiu5-ileoc-2qe` | [138360](https://dashboard.internetcomputer.org/proposal/138360) |
| Lukas Helebrandt | [lukas-helebrandt](node-providers/lukas-helebrandt/) | `efem5-kmwaw-xose7-zzhgg-6bfif-twmcw-csg7a-lmqvn-wrdou-mjwlb-vqe` | [119112](https://dashboard.internetcomputer.org/proposal/119112) |
| Maksym Ishchenko | [maksym-ishchenko](node-providers/maksym-ishchenko/) | `4r6qy-tljxg-slziw-zoteo-pboxh-vlctz-hkv2d-7zior-u3pxm-mmuxb-cae` | [125499](https://dashboard.internetcomputer.org/proposal/125499) |
| Mariano Stoll | [mariano-stoll](node-providers/mariano-stoll/) | `s5nvr-ipdxf-xg6wd-ofacm-7tl4i-nwjzx-uulum-cugwb-kbpsa-wrsgs-cae` | [127662](https://dashboard.internetcomputer.org/proposal/127662) |
| Marvelous Web3 | [marvelous-web3](node-providers/marvelous-web3/) | `7uioy-xitfw-yqcko-5gpya-3lpsw-dw7zt-dyyyf-wfqif-jvi76-fdbkg-cqe` | [122511](https://dashboard.internetcomputer.org/proposal/122511) |
| MB Patrankos šūvis | [mb-patrankos-suvis](node-providers/mb-patrankos-suvis/) | `4jjya-hlyyc-s766p-fd6gr-d6tvv-vo3ah-j5ptx-i73gw-mwgyd-rw6w2-rae` | [123923](https://dashboard.internetcomputer.org/proposal/123923) |
| MI Servers | [mi-servers](node-providers/mi-servers/) | `izmhk-lpjum-uo4oy-lviba-yctpc-arg4b-2ywim-vgoiu-gqaj2-gskmw-2qe` | none |
| ML SOLUTIONS LTD | [ml-solutions-ltd](node-providers/ml-solutions-ltd/) | `n6w7e-4cio3-an35h-hntwl-zzg4p-krqjk-yfmni-q7jiu-bage2-hef5b-pae` | [126312](https://dashboard.internetcomputer.org/proposal/126312) |
| Natalia Kulesha | [natalia-kulesha](node-providers/natalia-kulesha/) | `6ryfx-xszlo-xpvyj-b7vx6-m4erk-zwdkc-5lzfw-fty7k-arl66-uc3jk-nae` | [127688](https://dashboard.internetcomputer.org/proposal/127688) |
| Nataliia Nykyforak | [nataliia-nykyforak](node-providers/nataliia-nykyforak/) | `kf7dx-5wayj-3p2u4-yd4hf-m2en4-np75j-tta25-wqe7y-rlm6s-nqceb-7ae` | [127035](https://dashboard.internetcomputer.org/proposal/127035) |
| Neptune Partners | [neptune-partners](node-providers/neptune-partners/) | `4dibr-2alzr-h6kva-bvwn2-yqgsl-o577t-od46o-v275p-a2zov-tcw4f-eae` | [124507](https://dashboard.internetcomputer.org/proposal/124507) |
| Nikola Nikov | [nikola-nikov](node-providers/nikola-nikov/) | `kn4u4-unhbe-qwud4-ki6lq-o4try-6l2gv-yrxmg-vw6st-fmlss-nsztj-7qe` | [128151](https://dashboard.internetcomputer.org/proposal/128151) |
| NODAL CAPITAL | [nodal-capital](node-providers/nodal-capital/) | `kgfpq-4th36-lvnpn-ayygq-hikoq-dndag-vvafx-msvg5-aczmu-pkzsv-7ae` | [127704](https://dashboard.internetcomputer.org/proposal/127704) |
| NODAO | [nodao](node-providers/nodao/) | `g7dkt-aapqq-j3hqt-xtiys-pwapz-idulp-nwagd-zibqm-caxa4-gc23t-3qe` | [135317](https://dashboard.internetcomputer.org/proposal/135317) |
| NOKU SA | [noku-sa](node-providers/noku-sa/) | `64kb5-mzfmq-5wq5v-tm4p6-hekel-ne5xb-amiwr-cwvgg-t7db6-jlpau-nae` | [138174](https://dashboard.internetcomputer.org/proposal/138174) |
| NoviSystems, LLC | [novisystems-llc](node-providers/novisystems-llc/) | `hk7eo-22zam-kqmsx-dtfbj-k5i6f-jg65h-micpf-2cztc-t2eqk-efgvx-vqe` | [123307](https://dashboard.internetcomputer.org/proposal/123307) |
| OneSixtyTwo Digital Capital | [onesixtytwo-digital-capital](node-providers/onesixtytwo-digital-capital/) | `6nbcy-kprg6-ax3db-kh3cz-7jllk-oceyh-jznhs-riguq-fvk6z-6tsds-rqe` | none |
| Origin Game | [origin-game](node-providers/origin-game/) | `cgmhq-c4zja-yov4u-zeyao-64ua5-idlhb-ezcgr-cultv-3vqjs-dhwo7-rqe` | [125629](https://dashboard.internetcomputer.org/proposal/125629) |
| ParaFi Technologies NS LLC | [parafi-technologies-ns-llc](node-providers/parafi-technologies-ns-llc/) | `2hl5k-umjdt-ykii4-goecz-kkps6-nvl53-l7ost-p4mcp-qmnmw-rzrfc-mqe` | [137171](https://dashboard.internetcomputer.org/proposal/137171) |
| Pindar Technology Limited | [pindar-technology-limited](node-providers/pindar-technology-limited/) | `r3yjn-kthmg-pfgmb-2fngg-5c7d7-t6kqg-wi37r-j7gy6-iee64-kjdja-jae` | [116679](https://dashboard.internetcomputer.org/proposal/116679) |
| Power Meta Corporation | [power-meta-corporation](node-providers/power-meta-corporation/) | `4fedi-eu6ue-nd7ts-vnof5-hzg66-hgzl7-liy5n-3otyp-h7ipw-owycg-uae` | [124499](https://dashboard.internetcomputer.org/proposal/124499) |
| Privoxy Solutions, LLC | [privoxy-solutions-llc](node-providers/privoxy-solutions-llc/) | `trxbq-wy5xi-3y27q-bkpaf-mhi2m-puexs-yatgt-nhwiy-dh6jy-rolw5-zqe` | [125340](https://dashboard.internetcomputer.org/proposal/125340) |
| Protocol16 | [protocol16](node-providers/protocol16/) | `x7uok-pi537-itm37-unjn3-ewkze-kuetg-kptap-nuqak-auq7z-tn5ey-dqe` | [133135](https://dashboard.internetcomputer.org/proposal/133135) |
| Reist Telecom AG | [reist-telecom-ag](node-providers/reist-telecom-ag/) | `ma7dp-gz4tg-3c2wv-pgnsv-wna7u-czvhu-fpu47-t4dr6-gzxql-wr2m2-qae` | [135186](https://dashboard.internetcomputer.org/proposal/135186) |
| Rivram Inc | [rivram-inc](node-providers/rivram-inc/) | `ulyfm-vkxtj-o42dg-e4nam-l4tzf-37wci-ggntw-4ma7y-d267g-ywxi6-iae` | [91624](https://dashboard.internetcomputer.org/proposal/91624) |
| senseLAN | [senselan](node-providers/senselan/) | `f5kd2-ylls6-e6cts-6exqp-pwra3-djn2g-lnvbi-a3qs6-cfdr6-ti5dw-qqe` | [138399](https://dashboard.internetcomputer.org/proposal/138399) |
| Serenity Lotus Limited | [serenity-lotus-limited](node-providers/serenity-lotus-limited/) | `2cfu2-qyug6-y4cme-lvj3c-6fs65-cbti4-ea6ig-nkaoj-fsbte-7n5gp-wae` | [128867](https://dashboard.internetcomputer.org/proposal/128867) |
| SolNet | [solnet](node-providers/solnet/) | `mf6om-4m4yc-36jur-ip35a-6d3yr-kqi7v-txofz-nraz3-f6a4l-dcufx-oqe` | [138471](https://dashboard.internetcomputer.org/proposal/138471) |
| Starbase | [starbase](node-providers/starbase/) | `sixix-2nyqd-t2k2v-vlsyz-dssko-ls4hl-hyij4-y7mdp-ja6cj-nsmpf-yae` | none |
| Swiss Datalink AG | [swiss-datalink-ag](node-providers/swiss-datalink-ag/) | `hycj4-e3jwh-l2bqz-ohuxh-tu4af-agzov-uugg6-j57rk-b6opc-fx3ml-kqe` | [138385](https://dashboard.internetcomputer.org/proposal/138385) |
| Sygnum Bank | [sygnum-bank](node-providers/sygnum-bank/) | `6r5lw-l7db7-uwixn-iw5en-yy55y-ilbtq-e6gcv-g22r2-j3g6q-y37jk-jqe` | none |
| The Fenex Company LLC | [the-fenex-company-llc](node-providers/the-fenex-company-llc/) | `b7yyj-o7vc6-hdbzl-eggkm-bp2hg-3jmcv-5j5nn-t6zkq-ino4b-cvyde-yqe` | [127697](https://dashboard.internetcomputer.org/proposal/127697) |
| Uvaca Labs LLC | [uvaca-labs-llc](node-providers/uvaca-labs-llc/) | `dodsd-rsjlg-sgekb-gr6mi-l6fck-tscwk-4jzgl-fwk4q-ncoyu-ulx53-aqe` | [134532](https://dashboard.internetcomputer.org/proposal/134532) |
| vestra ICT AG | [vestra-ict-ag](node-providers/vestra-ict-ag/) | `izdfy-ocmaz-3qwcy-lluqx-tvq64-oybib-oyhxx-3dfni-ssznb-suhes-iqe` | [138470](https://dashboard.internetcomputer.org/proposal/138470) |
| Virtual Hive Ltd | [virtual-hive-ltd](node-providers/virtual-hive-ltd/) | `wdnqm-clqti-im5yf-iapio-avjom-kyppl-xuiza-oaz6z-smmts-52wyg-5ae` | none |
| Vladyslav Popov | [vladyslav-popov](node-providers/vladyslav-popov/) | `3oqw6-vmpk2-mlwlx-52z5x-e3p7u-fjlcw-yxc34-lf2zq-6ub2f-v63hk-lae` | [125610](https://dashboard.internetcomputer.org/proposal/125610) |
| Wancloud limited | [wancloud-limited](node-providers/wancloud-limited/) | `g2ax6-jrkmb-3zuh3-jibtb-q5xoq-njrgo-5utbc-j2o7g-zfq2w-yyhky-dqe` | [122357](https://dashboard.internetcomputer.org/proposal/122357) |
| Web3game | [web3game](node-providers/web3game/) | `64xe5-tx2s3-4gjmj-pnozr-fejw2-77y5y-rhcjk-glnmx-62brf-qin5q-pqe` | [125334](https://dashboard.internetcomputer.org/proposal/125334) |
| WMA Investments Limited | [wma-investments-limited](node-providers/wma-investments-limited/) | `7ne6c-3ahs2-76so4-te6hs-oq4mv-zhz4c-pqj2b-rxjmq-q56vn-tvpgj-2ae` | [128802](https://dashboard.internetcomputer.org/proposal/128802) |
| Wolkboer (Pty) Ltd | [wolkboer-pty-ltd](node-providers/wolkboer-pty-ltd/) | `mme7u-zxs3z-jq3un-fbaly-nllcz-toct2-l2kp3-larrb-gti4r-u2bmo-dae` | [124485](https://dashboard.internetcomputer.org/proposal/124485) |
| Zarety LLC | [zarety-llc](node-providers/zarety-llc/) | `glrjs-2dbzh-owbdd-fpp5e-eweoz-nsuto-e3jmk-tl42c-wem4f-qfpfa-qqe` | [134720](https://dashboard.internetcomputer.org/proposal/134720) |
| Zenith Code LLC | [zenith-code-llc](node-providers/zenith-code-llc/) | `pa5mu-yxsey-b4yrk-bodka-dhjnm-a3nx4-w2grw-3b766-ddr6e-nupu4-pqe` | [126384](https://dashboard.internetcomputer.org/proposal/126384) |
| Zondax AG | [zondax-ag](node-providers/zondax-ag/) | `hzqcb-iiagd-4erjo-qn7rq-syqro-zztl6-cpble-atnkd-2c6bg-bxjoa-qae` | [112706](https://dashboard.internetcomputer.org/proposal/112706) |
| ZTLC PTE LTD | [ztlc-pte-ltd](node-providers/ztlc-pte-ltd/) | `amsdj-4ss2k-wwcae-kroro-ippwx-lcro4-ysoha-uqlvc-3267j-vt3fy-yqe` | [126144](https://dashboard.internetcomputer.org/proposal/126144) |
