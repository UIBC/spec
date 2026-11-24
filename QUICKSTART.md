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

以下为 2026-11-24 在 `main@1f80a03` 上、Windows 11 / Python 3.13 的全新 clone 实跑原样输出（`--pubkey` 行会打印你本机的绝对路径）：

```
[OK] clean                        rc=0 result=PASS (expected rc=0 result=PASS)
[OK] clean --pubkey <你的路径>\keys\owner.key.pub rc=0 result=PASS (expected rc=0 result=PASS)
[OK] tampered                     rc=1 result=FAIL (expected rc=1 result=FAIL)
[OK] deleted                      rc=1 result=FAIL (expected rc=1 result=FAIL)
[OK] keyswap                      rc=0 result=PASS (expected rc=0 result=PASS)
[OK] keyswap --pubkey <你的路径>\keys\owner.key.pub rc=1 result=FAIL (expected rc=1 result=FAIL)

MATRIX GATE OK - all 6 rows match.
```

退出码 0 才算过。任何一行 `got` 与 `expect` 不同，脚本 exit 1。

## 3 · 查（一条）

```bash
python tools/check_key_hygiene.py
```

期望输出：`KEY HYGIENE OK - 53 tracked files, 4 pinned fixtures unchanged, no seed outside keys/`

（文件计数随提交增长会变，`4 pinned fixtures unchanged` 与 `no seed outside keys/` 两句才是判据。）

它钉死了四个测试密钥文件的摘要（`owner.key` / `owner.key.pub` / `attacker.key` / `attacker.key.pub`）。改动任一字节即红。

## 这六行到底在证明什么

| 行 | 它证明的 | 它**不**证明的 |
|---|---|---|
| 1–2 `clean` | 陌生人无密钥可验；钉住作者公钥仍 PASS | 作者真的做过这件事 |
| 3–4 `tampered` / `deleted` | 改了或删了一个证据文件，S4 会抓到 | 未被改动的部分就是真实的 |
| 5 `keyswap` open → **PASS** | 内部自洽：另一把钥匙重签的整包，会验成自己 | 这不是作者产的 |
| 6 `keyswap` pinned → FAIL | 钉公钥是唯一能抓到整包伪造的动作 | 钉的公钥本身可信 |

第 5 行写成 PASS 是有意的，它是本仓的核心口径：**不带钉定的 PASS 只说明包内自洽，不说明来源**。谁引用 UIBC 的 PASS 而没说是否钉定，就等于只引用了半条结果。

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
