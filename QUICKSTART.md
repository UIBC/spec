# QUICKSTART · 三条命令，读到本仓的真结论

本页只做一件事：让你在 clone 之后 **两分钟内** 得到和我一样的读数，不需要读 draft，也不需要问作者。

## 1 · 装（一条）

```bash
python -m pip install "uibc-core==0.5.0"
```

Python ≥ 3.10。**Windows 控制台**请先设 `PYTHONIOENCODING=utf-8`：0.5.0 会在 cp1252 控制台上打印中文 `basis.note` 时崩（`UnicodeEncodeError`），这是已知的上游缺陷，不是本仓的问题。

## 2 · 跑（一条）

```bash
git clone --depth 1 https://github.com/UIBC/vectors.git && cd vectors
python tools/run_vectors.py
```

期望输出（原样六行，顺序固定）：

以下为 2026-11-24 在 `UIBC/vectors` 合并后 main（`2f1f39b`）、Windows 11 / Python 3.13 的全新 clone 实跑原样输出（`--pubkey` 行会打印你本机的绝对路径）：

```
[OK] clean                        rc=0 result=PASS (expected rc=0 result=PASS)
[OK] clean --pubkey <你的路径>\keys\owner.key.pub rc=0 result=PASS (expected rc=0 result=PASS)
[OK] tampered                     rc=1 result=FAIL (expected rc=1 result=FAIL)
[OK] deleted                      rc=1 result=FAIL (expected rc=1 result=FAIL)
[OK] keyswap                      rc=0 result=PASS (expected rc=0 result=PASS)
[OK] keyswap --pubkey <你的路径>\keys\owner.key.pub rc=1 result=FAIL (expected rc=1 result=FAIL)
[OK] unsigned                     rc=1 result=INCONCLUSIVE (expected rc=1 result=INCONCLUSIVE)
[OK] unknown-upgrade              rc=1 result=INCONCLUSIVE (expected rc=1 result=INCONCLUSIVE)

MATRIX GATE OK - all 8 rows match.
```

退出码 0 才算过。任何一行 `got` 与 `expect` 不同，脚本 exit 1。

## 3 · 查（三条，各管一件事）

```bash
python tools/check_key_hygiene.py    # 密钥不被误提交、四个固件摘要未变
python tools/check_frozen.py         # 夹具字节 vs FIXTURES.sha256（45 个文件）
python tools/run_adversarial.py      # 12 个篡改包：9 个必须被拒，3 个是已登记缺陷
```

期望输出：

```
KEY HYGIENE OK - <N> tracked files, 4 pinned fixtures unchanged, no seed outside keys/
FROZEN OK - 45 fixture files match FIXTURES.sha256
[DEFECT] index-metadata-drift   rc=0 result=PASS   ... | D-002
[DEFECT] evidence-id-drift      rc=0 result=PASS   ... | D-002
[DEFECT] media-type-drift       rc=0 result=PASS   ... | D-002
ADVERSARIAL OK - 9/9 must-reject cases rejected; 3 documented gap(s) still reproduce.
```

文件计数会随提交变化；判据是 `4 pinned fixtures unchanged`、`no seed outside keys/`、`45 fixture files`。

**那三行 `[DEFECT]`是真发现，不是通过的测试。** 缺陷编号 D-002：索引摘要覆盖 `path`/`content_hash`/`type`/`note`，但**不覆盖** `evidence_id`、`media_type`、`created_at`——这三个字段被改写后判定仍是 PASS。后果是可回溯改时间、可换证据编号而不被发现。加 `--strict` 跑对抗集，会因这三条未修而失败；修好之后把三条移入 must-reject，`--strict` 才应该绿。**缺陷消失而台账没改，跑数本身会红**，所以这份清单不会腐坏。

它钉死了四个测试密钥文件的摘要（`owner.key` / `owner.key.pub` / `attacker.key` / `attacker.key.pub`）。改动任一字节即红。

## 这八行到底在证明什么

| 行 | 它证明的 | 它**不**证明的 |
|---|---|---|
| 1–2 `clean` | 陌生人无密钥可验；钉住作者公钥仍 PASS | 作者真的做过这件事 |
| 3–4 `tampered` / `deleted` | 改了或删了一个证据文件，S4 会抓到 | 未被改动的部分就是真实的 |
| 5 `keyswap` open → **PASS** | 内部自洽：另一把钥匙重签的整包，会验成自己 | 这不是作者产的 |
| 6 `keyswap` pinned → FAIL | 钉公钥是唯一能抓到整包伪造的动作 | 钉的公钥本身可信 |
| 7 `unsigned` → INCONCLUSIVE | 没有印章的包只能判"自洽但未背书"，不能判 PASS | 包里的证据是真的 |
| 8 `unknown-upgrade` → INCONCLUSIVE | manifest 自称 `PASS` 不构成证据，不能把 INCONCLUSIVE 升格 | 宣言之外还有任何依据 |

第 5 行写成 PASS 是有意的，它是本仓的核心口径：**不带钉定的 PASS 只说明包内自洽，不说明来源**。谁引用 UIBC 的 PASS 而没说是否钉定，就等于只引用了半条结果。第 7–8 行是同一件事的另一面：**说"我通过了"从来不等于通过**。

## 如果你要回一条 receipt（可选，成为 RUNS.md 的一行）

```bash
python tools/make_receipt.py --runner "<你的 handle>" --blind yes --code independent
python tools/check_receipt.py receipts/<你的文件>.json     # 期望：ACCEPTABLE
```

然后开一条 *Independent run receipt* issue 附上文件。receipt 记录的是一次运行 + 字节摘要，**不**证明运行者是谁，单条也不使本项目变成"已被外部验证"。

## 边界

- 这些向量演示的是 `uibc-core` 0.5.0 观测边界内的检出，不是"不存在未检出攻击"的证明，也不是第三方实现的一致性套件——**那套套件还没有**。
- 未做：乱序 / 回滚向量（回滚需要包外单调锚点）、跨实现回放。
- 完整期望表与已知缺口见 [`vectors/EXPECTED.md`](https://github.com/UIBC/vectors/blob/main/EXPECTED.md)，规范正文见 [`spec/draft-zhao-uibc-evidence-chain-00.md`](spec/draft-zhao-uibc-evidence-chain-00.md)。
