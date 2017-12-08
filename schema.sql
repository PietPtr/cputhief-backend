drop table if exists primes;
create table primes (
  number integer primary key,
  checked integer
);

drop table if exists blocks;
create table blocks (
  blocknum integer primary key,
  blocksize integer
);
