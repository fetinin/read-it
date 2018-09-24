export const updateArrayItem = <T>(arr: T[], item: T, compKey: keyof T): T[] =>
  arr.map((i) => (i[compKey] === item[compKey] ? item : i));

export const removeArrayItem = <T>(arr: T[], item: T, compKey: keyof T): T[] =>
  arr.filter((i) => i[compKey] !== item[compKey]);
