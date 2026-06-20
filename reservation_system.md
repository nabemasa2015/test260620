# 予約管理システム

## DB
```sql
CREATE TABLE reservations (
  uid VARCHAR(64) PRIMARY KEY,
  start_date DATETIME NOT NULL,
  status ENUM('予約中','予約済','キャンセル') NOT NULL
);
```

## API
- POST /reservations : 新規登録
- DELETE /reservations/{uid} : 削除
- PUT /reservations/{uid} : 変更
- GET /reservations?uid={uid} : UID検索
- GET /reservations?status={status} : ステータス検索

## サンプル(SQL)
INSERT INTO reservations(uid,start_date,status) VALUES(?,?,?);
DELETE FROM reservations WHERE uid=?;
UPDATE reservations SET start_date=?, status=? WHERE uid=?;
SELECT * FROM reservations WHERE uid=?;
SELECT * FROM reservations WHERE status=?;
