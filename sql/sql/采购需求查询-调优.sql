/* Formatted on 2014/8/7 14:36:43 (QP5 v5.256.13226.35538) */
SELECT bn2.need_Id needId,
       bn2.subject subject,
       bn2.last_update_time lastUpdateTime,
       bn2.need_type needType,
       SUBSTR (bnd.contents, 0, 30) content,
       bn2.expiry_date expiryDate,
       bn2.post_time postTime,
       bnd.PURCHASE_QTY purchaseQty,
       bn2.user_id userId,
       bn2.region_id regionId,
       bn2.country_id countryId,
       bnd.attachment attachment,
       bn2.intention intention,
       bn2.status status,
       bn2.confirmed confirm,
       bnd.namecard_photo namecardPhoto,
       bn2.create_time createTime,
       bn2.deleted_by_user,
       (SELECT COUNT (0)
          FROM im$buy_need_interest ibni
         WHERE     ibni.need_id = bn2.need_id
               AND ibni.is_favorited = :favourY
               AND ibni.user_id = :userId)
          isFavourited,
       (SELECT bnc.leaf_cat_id
          FROM buyer$need_cat bnc
         WHERE bnc.need_id = bnd.need_id)
          leafCatId
  FROM buyer$need_detail bnd, buyer$need bn2
 WHERE     bn2.need_id IN (SELECT bns.need_id
                             FROM (SELECT t.*, ROWNUM rowno
                                     FROM (  SELECT need_id
                                               FROM buyer$need bn
                                              WHERE     1 = 1
                                                    AND bn.is_public = :pubY
                                                    AND bn.status IN (7, 13)
                                                    AND (       bn.status = 7
                                                            AND (   bn.expiry_date IS NULL
                                                                 OR bn.expiry_date > SYSDATE)
                                                         OR EXISTS
                                                               (SELECT NULL
                                                                  FROM buyer$need_view_log bnvl
                                                                 WHERE     bnvl.need_id = bn.need_id
                                                                       AND EXISTS
                                                                              (SELECT NULL
                                                                                 FROM web$user wu
                                                                                WHERE     wu.comp_id = :sellerCompId
                                                                                      AND wu.user_id = bnvl.user_id)))
                                                    AND LOWER (bn.subject) LIKE :searchSubject
                                                    AND NOT EXISTS
                                                               (SELECT NULL
                                                                  FROM web$user wu,
                                                                       buyer$need_view_log bnvl
                                                                 WHERE     wu.comp_id = :sellerCompId
                                                                       AND wu.user_id = bnvl.user_id
                                                                       AND bnvl.need_id = bn.need_id)
                                           ORDER BY need_id DESC) t
                                    WHERE ROWNUM <= :maxSize) bns
                            WHERE bns.rowno > :minSize)
       AND bn2.need_id = bnd.need_id