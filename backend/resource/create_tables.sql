-- sqlite schema
-- department definition

CREATE TABLE "department" (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT NOT NULL, -- 部门名称
  `parent_id` INTEGER, -- 上级部门ID
  `manager_id` INTEGER, -- 部门负责人ID
  `create_time` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  `edit_time` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP -- 更新时间
);

CREATE UNIQUE INDEX uniq_department_name ON department (name);

-- employee definition

CREATE TABLE `employee` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `employee_no` TEXT NOT NULL, -- 员工编号
  `name` TEXT NOT NULL, -- 姓名
  `gender` INTEGER NOT NULL DEFAULT 0, -- 0-未知 1-男 2-女
  `birth_date` TEXT, -- 出生日期
  `phone` TEXT NOT NULL, -- 联系电话
  `email` TEXT NOT NULL, -- 电子邮箱
  `department_id` INTEGER NOT NULL, -- 所属部门
  `position` TEXT NOT NULL, -- 当前职位
  `entry_date` TEXT NOT NULL, -- 入职日期
  `status` INTEGER NOT NULL DEFAULT 2, -- 1-试用 2-在职 3-离职
  `create_time` TEXT DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  `edit_time` TEXT DEFAULT CURRENT_TIMESTAMP -- 更新时间
);

CREATE UNIQUE INDEX `uniq_employee_no` ON `employee` (`employee_no`);