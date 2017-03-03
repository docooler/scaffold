#!/bin/bash
patch_num=$1
ghead=""

sw_dir=/repo/path/swdir

if [ x"$patch_num" = x ]; then
        ghead="HEAD"
else
        ghead="HEAD^${patch_num}"
fi

cd ${sw_dir}
echo ${ghead}
git checkout dailySync
git remote update
commit_id=$(git rev-parse ${ghead})
echo "head is ${commit_id}"
git rebase --onto origin/master $commit_id dailySync
