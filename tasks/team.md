# AI Agent Team Structure

複数のAIエージェントが協調して開発タスクを遂行するためのチーム構成定義。

## Team Roles

### 1. Searcher（調査担当者）

**責任範囲:**
- コードベースの探索と理解
- 既存実装パターンの調査
- 関連ドキュメントの検索
- 外部リソース（ドキュメント、API仕様）の収集

**使用ツール:**
- `Grep`, `Glob`, `Read` - コード検索
- `Task(subagent_type=Explore)` - 深い探索
- `WebSearch`, `WebFetch` - 外部情報収集
- `mcp__context7__*` - ライブラリドキュメント検索

**アウトプット:**
- 調査レポート（関連ファイル、パターン、依存関係）
- 参考リンク・ドキュメント一覧

---

### 2. Architect（設計者）

**責任範囲:**
- システム設計・アーキテクチャ決定
- 技術選定の判断
- インターフェース定義
- 設計ドキュメントの作成

**使用ツール:**
- `Task(subagent_type=architect-reviewer)` - 設計レビュー
- `mcp__sequential-thinking__sequentialthinking` - 複雑な設計判断
- `Read`, `Grep` - 既存設計の確認

**アウトプット:**
- 設計ドキュメント（`tasks/design/*.md`）
- クラス図・シーケンス図（テキストベース）
- 技術選定の根拠

---

### 3. Planner（計画者）

**責任範囲:**
- タスクの分解と優先順位付け
- 実装ステップの定義
- 依存関係の特定
- リスク評価

**使用ツール:**
- `Task(subagent_type=Plan)` - 実装計画策定
- `TodoWrite` - タスク管理
- `EnterPlanMode` - 詳細計画モード

**アウトプット:**
- 実装計画（`tasks/todo.md`）
- チェックリスト形式のタスク一覧
- マイルストーン定義

---

### 4. Implementer（実装者）

**責任範囲:**
- コードの実装
- 単体テストの作成（TDD時）
- ドキュメントコメントの追加
- コードスタイルの遵守

**使用ツール:**
- `Edit`, `Write` - ファイル編集
- `mcp__serena__*` - シンボリック編集
- `Bash` - コマンド実行
- `LSP` - コード補完・定義ジャンプ

**アウトプット:**
- 実装コード
- インラインドキュメント
- 変更サマリー

---

### 5. Reviewer（レビュアー）

**責任範囲:**
- コード品質の確認
- セキュリティ脆弱性のチェック
- ベストプラクティスの適用確認
- パフォーマンス問題の検出

**使用ツール:**
- `Task(subagent_type=code-reviewer)` - コードレビュー
- `Task(subagent_type=security-auditor)` - セキュリティ監査
- `Bash(ruff:*, mypy:*)` - 静的解析

**アウトプット:**
- レビューコメント
- 改善提案リスト
- 承認/却下の判定

---

### 6. Tester（テスター）

**責任範囲:**
- テストケースの設計
- テストコードの実装
- テスト実行と結果分析
- カバレッジ確認

**使用ツール:**
- `Task(subagent_type=qa-expert)` - QA専門タスク
- `Bash(pytest:*, coverage:*)` - テスト実行
- `Skill(test-driven-development)` - TDDワークフロー

**アウトプット:**
- テストコード
- テスト結果レポート
- カバレッジレポート

---

### 7. Approver（承認者）

**責任範囲:**
- 最終品質確認
- マージ判断
- リリース承認
- ドキュメント完備確認

**使用ツール:**
- `Skill(verification-before-completion)` - 完了前検証
- `Skill(finishing-a-development-branch)` - ブランチ完了
- `Bash(git:*, gh:*)` - Git操作

**アウトプット:**
- 承認/却下判定
- マージ実行
- リリースノート

---

## Workflow

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│ Searcher │────▶│ Architect │────▶│ Planner  │
└──────────┘     └───────────┘     └──────────┘
                                         │
                                         ▼
┌──────────┐     ┌──────────┐     ┌─────────────┐
│ Approver │◀────│ Reviewer │◀────│ Implementer │
└──────────┘     └──────────┘     └─────────────┘
      │                ▲                  │
      │                │                  ▼
      │          ┌──────────┐             │
      │          │  Tester  │◀────────────┘
      │          └──────────┘
      │                │
      ▼                ▼
    [Merge]    [Test Results]
```

## Handoff Protocol

各役割間の引き継ぎルール:

### Searcher → Architect
- 調査結果サマリー
- 関連ファイルパス一覧
- 既存パターンの説明

### Architect → Planner
- 設計ドキュメント
- 技術的制約
- 推奨アプローチ

### Planner → Implementer
- タスクチェックリスト（`tasks/todo.md`）
- 優先順位
- 依存関係マップ

### Implementer → Reviewer
- 変更ファイル一覧
- 実装の意図説明
- 自己チェック結果

### Implementer → Tester
- テスト対象の説明
- 期待される動作
- エッジケース情報

### Reviewer → Approver
- レビュー結果サマリー
- 未解決の懸念事項
- 承認推奨/非推奨

### Tester → Approver
- テスト結果
- カバレッジ情報
- 品質メトリクス

---

## Usage Example

```bash
# 1. 調査フェーズ
claude --skill searcher "Excel読み込み機能の既存実装を調査"

# 2. 設計フェーズ
claude --skill architect "調査結果に基づいてダンプ機能を設計"

# 3. 計画フェーズ
claude --skill planner "設計に基づいて実装計画を作成"

# 4. 実装フェーズ
claude --skill implementer "計画に従って実装"

# 5. レビューフェーズ
claude --skill reviewer "実装をレビュー"

# 6. テストフェーズ
claude --skill tester "テストを作成・実行"

# 7. 承認フェーズ
claude --skill approver "最終確認とマージ"
```

---

## Notes

- 各役割は独立して実行可能だが、前フェーズのアウトプットを参照する
- 問題発見時は前フェーズにフィードバックし、必要に応じて再実行
- `tasks/` ディレクトリを中央リポジトリとして情報共有
- 全フェーズで `tasks/lessons.md` に学んだことを記録
