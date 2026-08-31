-- 批量新增激活码（在 Supabase Dashboard → SQL Editor 执行）
-- 注意：不要加 ON CONFLICT，因为 code 列没有唯一索引，加上会整条 INSERT 报错回滚
--   1. product_type 必须是 'goddess'，前端激活查询带了 .eq('product_type','goddess') 过滤
--   2. status 必须是 'unused'，激活后前端会改成 'used'
--   3. expires_at / activated_at 留空（NULL），用户激活时前端自动写入「激活时间 + 30天」
--   4. id 由数据库自增生成，无需指定

INSERT INTO public.activation_codes (code, status, product_type)
VALUES
  ('GODDESS-9EX7-FWHQ', 'unused', 'goddess'),
  ('GODDESS-5DLV-6YU5', 'unused', 'goddess'),
  ('GODDESS-EUBN-WYVR', 'unused', 'goddess'),
  ('GODDESS-4WVZ-L593', 'unused', 'goddess'),
  ('GODDESS-WPJP-5ENW', 'unused', 'goddess'),
  ('GODDESS-EF4D-6MR5', 'unused', 'goddess'),
  ('GODDESS-9HGE-GBBN', 'unused', 'goddess'),
  ('GODDESS-C7UY-H9QD', 'unused', 'goddess'),
  ('GODDESS-CSFN-X2KA', 'unused', 'goddess'),
  ('GODDESS-G275-KRD5', 'unused', 'goddess');

-- 执行后确认数量（应返回刚加的 10 行 unused）
SELECT code, status, product_type
FROM public.activation_codes
WHERE status = 'unused'
ORDER BY created_at DESC;
