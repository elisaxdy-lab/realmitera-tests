-- ============================================================
-- 希腊女神测试 · Supabase 一键配置脚本
-- 用途：激活码读取/核销 + 测试结果保存
-- 用法：Supabase Dashboard → SQL Editor 粘贴整段 → Run
-- ============================================================

-- 1. activation_codes：允许匿名查询未使用码 + 核销为 used
DROP POLICY IF EXISTS "allow_anon_select_activation_codes" ON public.activation_codes;
CREATE POLICY "allow_anon_select_activation_codes"
  ON public.activation_codes FOR SELECT TO anon USING (true);

DROP POLICY IF EXISTS "allow_anon_activate" ON public.activation_codes;
CREATE POLICY "allow_anon_activate"
  ON public.activation_codes FOR UPDATE TO anon
  USING (
    status = 'unused'
    AND product_type = 'goddess'
    AND (expires_at IS NULL OR expires_at > now())
  )
  WITH CHECK (status = 'used');

-- 2. test_results：建表（已存在则跳过）+ 开启 RLS + 允许匿名插入
CREATE TABLE IF NOT EXISTS public.test_results (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  code text,
  result_key text,
  secondary_key text,
  answers text,
  scores jsonb,
  user_agent text,
  device_id text,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE public.test_results ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "allow_anon_insert_results" ON public.test_results;
CREATE POLICY "allow_anon_insert_results"
  ON public.test_results FOR INSERT TO anon WITH CHECK (true);

GRANT INSERT, SELECT ON public.test_results TO anon;

-- 3. 验证：确认策略确实建上了（应看到 activation_codes 2 行 + test_results 1 行）
SELECT policyname, cmd, roles
FROM pg_policies
WHERE tablename IN ('activation_codes', 'test_results')
ORDER BY tablename;
