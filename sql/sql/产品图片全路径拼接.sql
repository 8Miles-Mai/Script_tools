/* Formatted on 2014/4/12 0:57:46 (QP5 v5.256.13226.35538) */
SELECT DECODE (
          INSTR (temp.thumbnail, 'group'),
          0, (   'http://newimg.globalmarket.com/piclib/'
              || MOD (temp.comp_id, 1000)
              || '/'
              || temp.comp_id
              || '/prod/'
              || temp.thumbnail),
          ('http://newimg.globalmarket.com/piclib/' || temp.thumbnail))
  FROM (SELECT sp.comp_id, sp.thumbnail
          FROM seller$product sp, seller$prod_tag spt
         WHERE     sp.comp_id = 2445788
               AND sp.status = 7
               AND spt.product_id = sp.product_id
               AND spt.tag_id = 2) temp